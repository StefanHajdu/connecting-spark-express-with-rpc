import grpc
import sparkapi_pb2
import sparkapi_session_pb2
import sparkapi_session_pb2_grpc
import multiprocessing as mp
import time

from concurrent import futures
from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)

from spark_session_instance import session_serve


class DuplicateSessionException(Exception):
    def __init__(self, message="Duplicate sessions"):
        super(DuplicateSessionException, self).__init__(message)


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

    def get_result_as_json(self, id, limit):
        return self.session_table[id].to_json(limit)

    def get_summary(self, id):
        return self.session_table[id].summarize()

    def session_info(self, id):
        return self.session_table[id].get_session_info()

    def print_session_table(self):
        print(self.session_table)
        for session_id, session in self.session_table:
            print(session_id)
            print(session.get_session_info())
            print()


BASE_SESSION_PORT = 50051

sessionTable = SessionTable()
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
        return sparkapi_pb2.PysparkGeneralResponse(
            id=res.id,
            msg=res.msg,
            columns_json=res.columns_json,
            num_rows=res.num_rows,
        )

    def createSession(
        self, req: sparkapi_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_pb2.NewSessionResponse:
        print(f"/createSession: {req.id}")

        # spawn new session server process
        session_port = get_new_port(sessionTable)
        session_server = mp_ctx.Process(
            target=session_serve, args=[session_port], daemon=True
        )
        session_server.start()

        # confirm connection
        print(
            f"confirming connection with session server -> id: {req.id} | port: {session_port}"
        )
        time.sleep(2)
        sessionTable.add(req.id, session_port)
        res = sessionTable.session_table[req.id]["stub"].createSession(
            sparkapi_session_pb2.NewSessionRequest(id=req.id)
        )

        # send response with child answer
        return sparkapi_pb2.NewSessionResponse(
            id=res.id,
            session_server_pid=res.session_server_pid,
            msg=res.msg,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkApiServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
