import grpc
import sparkapi_session_pb2
import os
import time

from concurrent import futures
from typing import Iterable
from sparkapi_session_pb2_grpc import (
    SparkApiSessionServicer,
    add_SparkApiSessionServicer_to_server,
)


class SparkApiSessionServicer(SparkApiSessionServicer):
    def previewDataset(
        self, req: sparkapi_session_pb2.PreviewDatasetRequest, unused_context
    ) -> Iterable[sparkapi_session_pb2.DatasetRowResponse]:
        print(f"[child] /preview: {req.id}, limit: {req.limit}")
        for row in ["row1"] * req.limit:
            time.sleep(0.5)
            row_json_obj = sparkapi_session_pb2.DatasetRowResponse(row_json=row)
            yield row_json_obj

    def loadsDataset(
        self, req: sparkapi_session_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkGeneralResponse:
        print(f"[child] /load: {req.id, req.df_path, req.df_type}")
        return sparkapi_session_pb2.PysparkGeneralResponse(
            id="id",
            msg="msg: data load",
            columns_json="columns",
            num_rows=0,
        )

    def createSession(
        self, req: sparkapi_session_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_session_pb2.NewSessionResponse:
        print(f"[child] /createSession: {req.id}")
        return sparkapi_session_pb2.NewSessionResponse(
            id=f"{req.id}", session_server_pid=f"{os.getpid()}", msg="session created"
        )


def session_serve(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_SparkApiSessionServicer_to_server(SparkApiSessionServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    print(f"Child session server is starting on {port}...")
    server.start()
    server.wait_for_termination()
