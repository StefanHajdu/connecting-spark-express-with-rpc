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
            id=res.id,
            msg=res.msg,
            columns_json=res.columns_json,
            num_rows=res.num_rows,
            schema_tree=res.schema_tree,
        )

    @sessionPlannerMap.spark_transformation_update
    def loadsDataset(
        self, req: sparkapi_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_pb2.PysparkGeneralResponse:
        print(f"/load: {req.id, req.df_path, req.df_type}")
        res = sessionTable.session_table[req.id]["stub"].loadsDataset(
            sparkapi_session_pb2.NewDatasetRequest(
                id=req.id,
                df_path=req.df_path,
                df_type=req.df_type,
            )
        )
        plan = SessionPlanner(
            {
                "node_id": PLAN_ROOT_ID,
                "op": "load",
                "df_path": req.df_path,
                "df_type": req.df_type,
            }
        )
        return (
            sparkapi_pb2.PysparkGeneralResponse(
                id=res.id,
                msg=res.msg,
                columns_json=res.columns_json,
                num_rows=res.num_rows,
                schema_tree=res.schema_tree,
            ),
            plan,
        )

    @sessionPlannerMap.spark_transformation_update
    def loadFromSession(
        self, req: sparkapi_pb2.DatasetFromSessionRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/loadFromSession: {req.id, req.input_id}")
        res = sessionTable.session_table[req.id]["stub"].loadFromSession(
            sparkapi_session_pb2.DatasetFromSessionRequest(
                id=req.id,
                input_id=req.input_id,
            )
        )

        plan = SessionPlanner(
            {"node_id": PLAN_ROOT_ID, "op": "loadFromSession", "input_id": req.input_id}
        )
        return (
            sparkapi_pb2.PysparkTransformResponse(
                id=res.id,
                msg=res.msg,
            ),
            plan,
        )

    @sessionPlannerMap.spark_transformation_update
    def runSql(
        self, req: sparkapi_pb2.SqlRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        print(
            f"/sql: {req.id, req.parametrized_query, req.query_name, req.params_json}"
        )
        res = sessionTable.session_table[req.id]["stub"].runSql(
            sparkapi_session_pb2.SqlRequest(
                id=req.id,
                parametrized_query=req.parametrized_query,
                query_name=req.query_name,
                params_json=req.params_json,
            )
        )

        req_log = {
            "op": "sql",
            "parametrized_query": req.parametrized_query,
            "query_name": req.query_name,
            "params_json": req.params_json,
        }

        return (
            sparkapi_pb2.PysparkTransformResponse(
                id=res.id,
                msg=res.msg,
            ),
            req_log,
        )

    def rebuildSession(
        self, req: sparkapi_pb2.RebuildRequest, unused_context
    ) -> sparkapi_pb2.PysparkTransformResponse:
        print(f"/rebuildSession: {req.id}")
        res = sessionTable.session_table[req.id]["stub"].rebuildSession(
            sparkapi_session_pb2.RebuildRequest(
                id=req.id, log_json=sessionPlannerMap.get_plan(req.id)
            )
        )
        return sparkapi_pb2.PysparkTransformResponse(id=res.id, msg=res.msg)

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
            id=req.id, plan_deque=sessionPlannerMap.get_plan_pickled(req.id)
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
