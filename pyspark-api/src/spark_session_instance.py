import grpc
import sparkapi_session_pb2
import os
import time
import json

from pyspark.sql import SparkSession

from concurrent import futures
from typing import Iterable
from sparkapi_session_pb2_grpc import (
    SparkApiSessionServicer,
    add_SparkApiSessionServicer_to_server,
)


class SparkApiSession:
    def __init__(self, pid, spark):
        self.pid = pid
        self.spark = spark
        self.df = None

    def set_id(self, id):
        self.id = id

    def load_dataset(self, path, df_type):
        self.df = self.read_spark_df(path, df_type)
        self.eager_cache()
        print(f"dataset `{path}` loaded")

    def read_spark_df(self, path: str, dataset_type: str):
        if dataset_type == "csv":
            return (
                self.spark.read.option("delimiter", ";")
                .option("header", True)
                .csv(path)
            )
        elif dataset_type == "json":
            return self.spark.read.json(path)

    def summarize(self):
        cols = json.dumps(self.df.columns)
        num_rows = self.df.count()
        return cols, num_rows

    def eager_cache(self):
        self.df.cache().count()

    def to_json(self, limit):
        return self.df.limit(limit).toPandas().to_json(orient="records")

    def get_session_info(self):
        return f"session: {self.spark_session},\ndf: {self.df.count()}"


spark = (
    SparkSession.builder.appName("SparkSession")
    .master("local[1]")
    .config("spark.driver.memory", "5096m")
    .config("spark.driver.cores", "4")
    .getOrCreate()
)
session = SparkApiSession(os.getpid(), spark)


class SparkApiSessionServicer(SparkApiSessionServicer):
    def previewDataset(
        self, req: sparkapi_session_pb2.PreviewDatasetRequest, unused_context
    ) -> Iterable[sparkapi_session_pb2.DatasetRowResponse]:
        print(f"[child] /preview: {req.id}, limit: {req.limit}")

        json_str_rows = session.to_json(req.limit)
        for row in json.loads(json_str_rows):
            time.sleep(0.5)
            row_json_obj = sparkapi_session_pb2.DatasetRowResponse(
                row_json=json.dumps(row)
            )
            yield row_json_obj

    def loadsDataset(
        self, req: sparkapi_session_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkGeneralResponse:
        print(f"[child] /load: {req.id, req.df_path, req.df_type}")

        session.load_dataset(req.df_path, req.df_type)
        columns, num_rows = session.summarize()

        return sparkapi_session_pb2.PysparkGeneralResponse(
            id=session.id,
            msg="msg: data load",
            columns_json=columns,
            num_rows=num_rows,
        )

    def createSession(
        self, req: sparkapi_session_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_session_pb2.NewSessionResponse:
        print(f"[child] /createSession: {req.id}")
        session.set_id(req.id)
        print(f"spark session init: {session.spark}")

        return sparkapi_session_pb2.NewSessionResponse(
            id=f"{session.id}",
            session_server_pid=f"{session.pid}",
            msg="session created",
        )


def session_serve(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_SparkApiSessionServicer_to_server(SparkApiSessionServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    print(f"Child session server is starting on {port}...")
    server.start()
    server.wait_for_termination()
