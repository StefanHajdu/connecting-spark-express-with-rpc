import grpc
from concurrent import futures
import sparkapi_pb2
import json
from pyspark.sql import SparkSession
import time

from typing import Iterable
from sparkapi_pb2_grpc import (
    SparkApiServicer,
    add_SparkApiServicer_to_server,
)


class DuplicateSessionException(Exception):
    def __init__(self, message="Duplicate sessions"):
        super(DuplicateSessionException, self).__init__(message)


spark = (
    SparkSession.builder.appName("SparkSession")
    .master("local[1]")
    .config("spark.driver.memory", "2048m")
    .config("spark.driver.cores", "2")
    .getOrCreate()
)


def read_spark_df(spark_session: SparkSession, path: str, dataset_type: str):
    if dataset_type == "csv":
        return (
            spark_session.read.option("delimiter", ",").option("header", True).csv(path)
        )
    elif dataset_type == "json":
        return spark_session.read.json(path)


class SparkApiSession:
    def __init__(self, path, df_type):
        self.spark_session = spark.newSession()
        self.df = read_spark_df(self.spark_session, path, df_type)

    def summarize(self):
        cols = json.dumps(self.df.columns)
        rows = self.df.count()
        return cols, rows

    def eager_cache(self):
        self.df.cache().count()

    def to_json(self, limit):
        return self.df.limit(limit).toPandas().to_json(orient="records")

    def get_session_info(self):
        return f"session: {self.spark_session},\ndf: {self.df.limit(10).show()}"


class SparkSessionTable:
    def __init__(self):
        self.session_table = {}

    def add(self, id, path, df_type):
        if id in self.session_table:
            raise DuplicateSessionException()
        self.session_table[id] = SparkApiSession(path, df_type)

    def get_result_as_json(self, id, limit):
        return self.session_table[id].to_json(limit)

    def get_summary(self, id):
        return self.session_table[id].summarize()

    def session_info(self, id):
        return self.session_table[id].get_session_info()


s = SparkSessionTable()


class SparkApiServicer(SparkApiServicer):
    def previewDataset(
        self, req: sparkapi_pb2.PreviewDatasetRequest, unused_context
    ) -> Iterable[sparkapi_pb2.DatasetRowResponse]:
        print(f"preview for id: {req.id}")
        json_str_rows = s.get_result_as_json(req.id, req.limit)
        for row in json.loads(json_str_rows):
            time.sleep(0.5)
            row_json_obj = sparkapi_pb2.DatasetRowResponse(row_json=json.dumps(row))
            yield row_json_obj

    def loadsDataset(
        self, req: sparkapi_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_pb2.PysparkGeneralResponse:
        try:
            s.add(req.id, req.df_path, req.df_type)
            columns, rows = s.get_summary(req.id)
            return sparkapi_pb2.PysparkGeneralResponse(
                id=req.id,
                msg=f"dataset loaded",
                columns_json=columns,
                num_rows=rows,
            )
        except DuplicateSessionException as e:
            columns, rows = s.get_summary(req.id)
            return sparkapi_pb2.PysparkGeneralResponse(
                id=req.id,
                msg=f"dataset already loaded with {s.session_info(req.id)}",
                columns_json=columns,
                num_rows=rows,
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SparkApiServicer_to_server(SparkApiServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
