import grpc
import multiprocessing as mp
import time
import json
import hashlib

import sparkapi_pb2
import sparkapi_session_pb2
import sparkapi_session_pb2_grpc

from functools import wraps
from concurrent import futures
from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)

from spark_session_instance import session_serve


class DuplicateSessionException(Exception):
    def __init__(self, message="Duplicate sessions"):
        super().__init__(message)


class SessionLogger:
    def __init__(self):
        self.session_logs = {}

    def init_log(self, id: str):
        self.session_logs.update({id: {"logs": [], "state_hash": None}})

    def get_log(self, id: str):
        return json.dumps(self.session_logs.get(id, {}).get("logs", {}))

    def _hash_log_state(self, id: str):
        self.session_logs[id]["state_hash"] = hashlib.sha256(
            str(self.session_logs[id]["logs"]).encode("utf-8")
        ).hexdigest()

    def log_request(self, func):
        """Adds rest api query to session log. Log is defined by session id.
        Init propagation of the change to child sessions.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            grpc_response_obj, request_log = func(*args, **kwargs)
            session_id = grpc_response_obj.id
            self.session_logs[session_id]["logs"].append(request_log)
            self.handle_log_change(session_id)
            return grpc_response_obj

        return wrapper

    def handle_log_change(self, id):
        """Get session ids that use current session as input. And send new query log."""
        ids_to_notify = self._get_session_dependency(id)
        for id_to_notify in ids_to_notify:
            self._notify_input_change(id_to_notify)

    def _get_session_dependency(self, master_session_id):
        """Filter only session that log plan starts with `loadFromSession` and uses this session id as input."""
        ls = []
        for id, log_obj in self.session_logs.items():
            for log in log_obj["logs"]:
                if (
                    log["op"] == "loadFromSession"
                    and log["input_id"] == master_session_id
                ):
                    ls.append(id)
                    break
        return ls

    def _notify_input_change(self, id: str):
        _ = sessionTable.session_table[id]["stub"].rebuildMasterDataframe(
            sparkapi_session_pb2.RebuildRequest(
                id=id,
                log_json=self.get_log(id),
            )
        )


class SessionTable:
    def __init__(self):
        self.session_table = {}

    def add(self, id, port):
        if id in self.session_table:
            raise DuplicateSessionException()
        else:
            channel = grpc.insecure_channel(f"localhost:{port}")
            stub = sparkapi_session_pb2_grpc.SparkApiSessionStub(channel)
            self.session_table.update(
                {id: {"port": port, "channel": channel, "stub": stub}}
            )


BASE_SESSION_PORT = 50051

sessionTable = SessionTable()
sessionLogger = SessionLogger()
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

    @sessionLogger.log_request
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
        req_log = {"op": "load", "df_path": req.df_path, "df_type": req.df_type}
        return (
            sparkapi_pb2.PysparkGeneralResponse(
                id=res.id,
                msg=res.msg,
                columns_json=res.columns_json,
                num_rows=res.num_rows,
                schema_tree=res.schema_tree,
            ),
            req_log,
        )

    @sessionLogger.log_request
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

        req_log = {"op": "loadFromSession", "input_id": req.input_id}
        return (
            sparkapi_pb2.PysparkTransformResponse(
                id=res.id,
                msg=res.msg,
            ),
            req_log,
        )

    @sessionLogger.log_request
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

    def createSession(
        self, req: sparkapi_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_pb2.NewSessionResponse:
        print(f"/createSession: {req.id}")

        # try to add new session
        session_port = get_new_port(sessionTable)
        sessionTable.add(req.id, session_port)
        sessionLogger.init_log(req.id)

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

    def getMasterDataframeLog(
        self, req: sparkapi_pb2.LogRequest, unused_context
    ) -> sparkapi_pb2.LogResponse:
        return sparkapi_pb2.LogResponse(
            id=req.id, log_json=sessionLogger.get_log(req.id)
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkApiServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
