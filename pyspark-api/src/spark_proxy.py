import grpc
import multiprocessing as mp
import time

import sparkapi_pb2
import sparkapi_session_pb2

from concurrent import futures
from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)

from spark_session_instance import session_serve
from PipelinePlan import SessionPlanner, SessionPlannerMap
from SessionTable import SessionTable


BASE_SESSION_PORT = 50051
PLAN_ROOT_ID = "0000-0000-0000"

sessionTable = SessionTable()
sessionPlannerMap = SessionPlannerMap(sessionTable)
mp_ctx = mp.get_context("spawn")


def get_new_port(s: SessionTable) -> int:
    return BASE_SESSION_PORT + len(s.session_table.keys()) + 1


class SparkApiServicer(SparkApiServicer):
    def previewDataset(
        self, req: sparkapi_pb2.PreviewDatasetRequest, unused_context
    ) -> Iterable[sparkapi_pb2.DatasetRowResponse]:
        print(f"/preview: {req.id}")
        res = sessionTable.session_table[req.id]["stub"].previewDataset(
            sparkapi_session_pb2.PreviewDatasetRequest(
                id=req.id,
                limit=req.limit,
            )
        )
        for datasetRowResponse in res:
            yield datasetRowResponse

    def summarizeDataset(
        self, req: sparkapi_pb2.SummarizeDatasetRequest, unused_context
    ) -> sparkapi_pb2.PysparkGeneralResponse:
        print(f"/summarize: {req.id}")
        res = sessionTable.session_table[req.id]["stub"].summarizeDataset(
            sparkapi_session_pb2.SummarizeDatasetRequest(id=req.id)
        )
        return sparkapi_pb2.PysparkGeneralResponse(
            session_id=res.session_id,
            msg=res.msg,
            columns_json=res.columns_json,
            num_rows=res.num_rows,
            schema_tree=res.schema_tree,
        )

    @sessionPlannerMap.spark_transformation_update
    def loadsDataset(
        self, req: sparkapi_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_pb2.PysparkGeneralResponse:
        print(f"/load: {req.session_id, req.df_path, req.df_type}")
        res = sessionTable.session_table[req.session_id]["stub"].loadsDataset(
            sparkapi_session_pb2.NewDatasetRequest(
                session_id=req.session_id,
                df_path=req.df_path,
                df_type=req.df_type,
            )
        )

        return (
            sparkapi_pb2.PysparkGeneralResponse(
                session_id=res.session_id,
                msg=res.msg,
                columns_json=res.columns_json,
                num_rows=res.num_rows,
                schema_tree=res.schema_tree,
            ),
            SessionPlanner(
                {
                    "node_id": PLAN_ROOT_ID,
                    "previous_node_id": None,
                    "op": "load",
                    "df_path": req.df_path,
                    "df_type": req.df_type,
                }
            ),
        )

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
                    "node_id": PLAN_ROOT_ID,
                    "previous_node_id": None,
                    "op": "loadFromSession",
                    "input_id": req.input_id,
                }
            ),
        )

    @sessionPlannerMap.spark_transformation_update
    def addSql(
        self, req: sparkapi_pb2.SqlRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
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
        return sparkapi_pb2.PysparkTransformResponse(
            session_id=res.session_id, msg=res.msg
        )

    def createSession(
        self, req: sparkapi_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_pb2.NewSessionResponse:
        print(f"/createSession: {req.id}")

        # try to add new session
        session_port = get_new_port(sessionTable)
        sessionTable.add(req.id, session_port)
        sessionPlannerMap.add_session(req.id)

        # spawn new session server process
        session_server = mp_ctx.Process(
            target=session_serve, args=[session_port], daemon=True
        )
        session_server.start()

        # confirm connection
        time.sleep(2)
        res = sessionTable.session_table[req.id]["stub"].createSession(
            sparkapi_session_pb2.NewSessionRequest(id=req.id)
        )

        # send response with child answer
        return sparkapi_pb2.NewSessionResponse(
            id=res.id,
            session_server_pid=res.session_server_pid,
            msg=res.msg,
        )

    def getParentSessionPlan(
        self, req: sparkapi_pb2.PlanRequest, unused_context
    ) -> sparkapi_pb2.PlanResponse:
        return sparkapi_pb2.PlanResponse(
            id=req.id, planner=sessionPlannerMap.get_planner_pickled(req.id)
        )

    def getRebuildStatus(
        self, req: sparkapi_pb2.RebuildStatusRequest, unused_context
    ) -> sparkapi_pb2.RebuildStatusResponse:
        print(f"/rebuildStatus: {req.id}")
        res = sessionTable.session_table[req.id]["stub"].getRebuildStatus(
            sparkapi_session_pb2.RebuildStatusRequest(id=req.id)
        )
        return sparkapi_pb2.RebuildStatusResponse(
            id=req.id, rebuild_status=res.rebuild_status
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkApiServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
