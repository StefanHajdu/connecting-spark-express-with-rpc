import grpc

from pyspark.sql import SparkSession

import sparkapi_pb2
import sparkapi_session_pb2

from concurrent import futures
from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)

from ClientSession import ClientSession
from SessionTable import SessionTable, ClientSessionTable
from PipelinePlan import SessionPlanner, SessionPlannerMap
from constants import BASE_SESSION_PORT, PLAN_NODE_ROOT_ID


sessionTable = SessionTable()
clientSessionTable = ClientSessionTable()
sessionPlannerMap = SessionPlannerMap(sessionTable)


def get_new_port(s: SessionTable) -> int:
    return BASE_SESSION_PORT + len(s.session_table.keys()) + 1


class SparkApiServicer(SparkApiServicer):
    @sessionPlannerMap.spark_transformation_update
    def loadFromSession(
        self, req: sparkapi_pb2.DatasetFromSessionRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/loadFromSession: {req.session_id, req.input_id}")
        res = sessionTable.session_table[req.session_id]["stub"].loadFromSession(
            sparkapi_session_pb2.DatasetFromSessionRequest(
                id=req.session_id,
                input_id=req.input_id,
            )
        )

        return (
            sparkapi_pb2.PysparkTransformResponse(
                session_id=res.session_id,
                msg=res.msg,
            ),
            SessionPlanner(
                {
                    "node_id": PLAN_NODE_ROOT_ID,
                    "previous_node_id": None,
                    "op": "loadFromSession",
                    "input_id": req.input_id,
                }
            ),
        )

    @sessionPlannerMap.spark_transformation_update
    def addSql(self, req: sparkapi_pb2.SqlRequest, unused_context) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/addSql: {req.session_id, req.query, req.previous_node_id:}")
        res = sessionTable.session_table[req.session_id]["stub"].addSql(
            sparkapi_session_pb2.SqlRequest(
                session_id=req.session_id,
                node_id=req.node_id,
                previous_node_id=req.previous_node_id,
                query_type=req.query_type,
                query=req.query,
                query_params_json=req.query_params_json,
                planner=sessionPlannerMap.get_planner_pickled(req.session_id),
            )
        )

        return (
            sparkapi_pb2.PysparkTransformResponse(
                session_id=res.session_id,
                msg=res.msg,
            ),
            res.planner,
        )

    @sessionPlannerMap.spark_transformation_update
    def editSql(self, req: sparkapi_pb2.SqlRequest, unused_context) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/editSql: {req.session_id, req.query, req.previous_node_id}")
        res = sessionTable.session_table[req.session_id]["stub"].editSql(
            sparkapi_session_pb2.SqlRequest(
                session_id=req.session_id,
                node_id=req.node_id,
                query_type=req.query_type,
                query=req.query,
                query_params_json=req.query_params_json,
                include_sql=req.include_sql,
                planner=sessionPlannerMap.get_planner_pickled(req.session_id),
            )
        )

        return (
            sparkapi_pb2.PysparkTransformResponse(
                session_id=res.session_id,
                msg=res.msg,
            ),
            res.planner,
        )

    @sessionPlannerMap.spark_transformation_update
    def removeSql(self, req: sparkapi_pb2.SqlRemovalRequest, unused_context) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/removeSql: {req.session_id, req.node_id, req.temp}")
        res = sessionTable.session_table[req.session_id]["stub"].removeSql(
            sparkapi_session_pb2.SqlRemovalRequest(
                session_id=req.session_id,
                node_id=req.node_id,
                temp=req.temp,
                planner=sessionPlannerMap.get_planner_pickled(req.session_id),
            )
        )

        return (
            sparkapi_pb2.PysparkTransformResponse(
                session_id=res.session_id,
                msg=res.msg,
            ),
            res.planner,
        )

    def rebuildSession(
        self, req: sparkapi_pb2.RebuildRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/rebuildSession: {req.session_id}")
        res = sessionTable.session_table[req.session_id]["stub"].rebuildSession(
            sparkapi_session_pb2.RebuildRequest(
                session_id=req.session_id,
                planner=sessionPlannerMap.get_planner_pickled(req.session_id),
            )
        )
        return sparkapi_pb2.PysparkTransformResponse(session_id=res.session_id, msg=res.msg)

    # refactor -->

    def createSession(self, req: sparkapi_pb2.NewSessionRequest, unused_context) -> sparkapi_pb2.NewSessionResponse:
        clientSessionTable.add(req.id, ClientSession(req.id))

        return sparkapi_pb2.NewSessionResponse(
            id=req.id,
            msg=f"Session {req.id} created.",
        )

    def loadsDataset(
        self, req: sparkapi_pb2.LoadDatasetRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.plan = SessionPlanner(req.session_id, session.load_dataset(spark, req.df_path, req.df_type))

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id, msg=f"Dataset {req.df_path} loaded.", schema="schema TO BE PROVIDED"
        )

    def summarizeDataset(
        self, req: sparkapi_pb2.SummarizeDatasetRequest, unused_context
    ) -> sparkapi_pb2.SparkActionlResponse:
        session = clientSessionTable.get_session(req.session_id)
        summary = session.summarize(req.node_id)

        return sparkapi_pb2.SparkActionlResponse(
            session_id=req.session_id,
            msg=f"Node {req.node_id} summarized",
            columns=summary["columns"],
            count=summary["count"],
            schema=summary["schema"],
        )

    def previewDataset(
        self, req: sparkapi_pb2.PreviewDatasetRequest, unused_context
    ) -> Iterable[sparkapi_pb2.RowStreamResponse]:
        session = clientSessionTable.get_session(req.session_id)
        row_stream = session.preview(req.node_id, req.limit)

        for row in row_stream:
            yield sparkapi_pb2.RowStreamResponse(row_json=row)

    def getParentSessionPlan(self, req: sparkapi_pb2.PlanRequest, unused_context) -> sparkapi_pb2.PlanResponse:
        return sparkapi_pb2.PlanResponse(id=req.id, planner=sessionPlannerMap.get_planner_pickled(req.id))

    def getRebuildStatus(
        self, req: sparkapi_pb2.RebuildStatusRequest, unused_context
    ) -> sparkapi_pb2.RebuildStatusResponse:
        print(f"/rebuildStatus: {req.id}")
        res = sessionTable.session_table[req.id]["stub"].getRebuildStatus(
            sparkapi_session_pb2.RebuildStatusRequest(id=req.id)
        )
        return sparkapi_pb2.RebuildStatusResponse(id=req.id, rebuild_status=res.rebuild_status)


spark = (
    SparkSession.builder.appName("SparkSession")
    .master("local[*]")
    .config("spark.driver.memory", "30720m")
    .getOrCreate()
)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkApiServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
