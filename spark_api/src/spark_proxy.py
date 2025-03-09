import grpc

from pyspark.sql import SparkSession

import sparkapi_pb2

from concurrent import futures
from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)

from ClientSession import ClientSession
from ClientSessionTable import ClientSessionTable
from PipelinePlan import SessionPlanner, SessionPlannerMap

clientSessionTable = ClientSessionTable()
sessionPlannerMap = SessionPlannerMap(clientSessionTable)


class SparkApiServicer(SparkApiServicer):
    # def rebuildSession(
    #     self, req: sparkapi_pb2.RebuildRequest, unused_context
    # ) -> sparkapi_pb2.PysparkTransformResponse:
    #     print(f"/rebuildSession: {req.session_id}")
    #     res = sessionTable.session_table[req.session_id]["stub"].rebuildSession(
    #         sparkapi_session_pb2.RebuildRequest(
    #             session_id=req.session_id,
    #             planner=sessionPlannerMap.get_planner_pickled(req.session_id),
    #         )
    #     )
    #     return sparkapi_pb2.PysparkTransformResponse(session_id=res.session_id, msg=res.msg)

    # def getParentSessionPlan(self, req: sparkapi_pb2.PlanRequest, unused_context) -> sparkapi_pb2.PlanResponse:
    #     return sparkapi_pb2.PlanResponse(id=req.id, planner=sessionPlannerMap.get_planner_pickled(req.id))

    # def getRebuildStatus(
    #     self, req: sparkapi_pb2.RebuildStatusRequest, unused_context
    # ) -> sparkapi_pb2.RebuildStatusResponse:
    #     print(f"/rebuildStatus: {req.id}")
    #     res = sessionTable.session_table[req.id]["stub"].getRebuildStatus(
    #         sparkapi_session_pb2.RebuildStatusRequest(id=req.id)
    #     )
    #     return sparkapi_pb2.RebuildStatusResponse(id=req.id, rebuild_status=res.rebuild_status)

    # refactor -->

    def createSession(self, req: sparkapi_pb2.NewSessionRequest, unused_context) -> sparkapi_pb2.NewSessionResponse:
        clientSessionTable.add(req.id, ClientSession(req.id))
        sessionPlannerMap.add_session(req.id)

        return sparkapi_pb2.NewSessionResponse(
            id=req.id,
            msg=f"Session {req.id} created.",
        )

    def loadsDataset(
        self, req: sparkapi_pb2.LoadDatasetRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        root_plan_node = session.load_dataset(spark, req.df_path, req.df_type)
        session.plan = SessionPlanner(req.session_id, root_plan_node)
        sessionPlannerMap.update_session_plan(session.id, session.plan)

        return sparkapi_pb2.SparkTransformResponse(session_id=req.session_id, msg=f"Dataset {req.df_path} loaded.")

    def loadFromSession(
        self, req: sparkapi_pb2.LoadFromSessionRequest, unused_context
    ) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        input_session_plan = sessionPlannerMap.get_session_plan(req.input_session_id)
        root_plan_node = session.load_from_session(input_session_plan)
        session.plan = SessionPlanner(req.session_id, root_plan_node)
        sessionPlannerMap.update_session_plan(session.id, session.plan)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Dataframe from input session {req.input_session_id} reused input.",
        )

    def addNode(self, req: sparkapi_pb2.NodeAddRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.add_node(
            spark=spark,
            node_id=req.node_id,
            prev_node_id=req.prev_node_id,
            query=req.query,
            query_type=req.query_type,
            query_params_json=req.query_params_json,
        )

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} added and transform: {req.query} applied",
        )

    def editNode(self, req: sparkapi_pb2.NodeEditRequest, unused_context) -> sparkapi_pb2.SparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.edit_node(spark, req.node_id, req.query_type, req.query, req.query_params_json)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} edited and transform: {req.query} applied",
        )

    def removeNode(
        self, req: sparkapi_pb2.NodeRemovalRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        session = clientSessionTable.get_session(req.session_id)
        session.remove_node(spark, req.node_id)

        return sparkapi_pb2.SparkTransformResponse(
            session_id=req.session_id,
            msg=f"Node: {req.node_id} removed",
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
