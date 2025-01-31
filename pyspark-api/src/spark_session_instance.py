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


class DfUtils:
    @classmethod
    def eager_cache_df(cls, df):
        df.cache().count()

    @classmethod
    def filter_df(cls, df, filter_sql):
        return df.filter(filter_sql)

    @classmethod
    def read_spark_df(cls, spark, path: str, dataset_type: str):
        if dataset_type == "csv":
            return spark.read.option("delimiter", ";").option("header", True).csv(path)
        elif dataset_type == "json":
            return spark.read.json(path)


class SparkApiSession:
    def __init__(self, pid, spark):
        self.pid = pid
        self.spark = spark
        self.df_init = None
        self.df_current = None

    # setters:

    def set_id(self, id):
        self.id = id

    # utilities:

    def check_load(self):
        return True if self.df_current else False

    def log_(self, msg):
        print(f"    [child_session-{self.id}] " + msg)

    def get_session_info(self):
        return f"session: {self.spark_session},\ndf: {self.df_current.count()}"

    # spark actions:

    def spark_action_load_dataset(self, path, df_type):
        self.df_init = self.df_current = DfUtils.read_spark_df(
            self.spark, path, df_type
        )
        DfUtils.eager_cache_df(self.df_current)
        DfUtils.eager_cache_df(self.df_init)
        print(f"dataset `{path}` loaded")

    def spark_action_summarize(self):
        # schema to str: schemaString = self.df_current._jdf.schema().treeString()
        self.df_current.printSchema()
        cols = json.dumps(self.df_current.columns)
        num_rows = self.df_current.count()
        return cols, num_rows

    def spark_action_to_json(self, limit):
        return self.df_current.limit(limit).toPandas().to_json(orient="records")

    def get_general_spark_response(self):
        columns, num_rows = self.spark_action_summarize()

        return sparkapi_session_pb2.PysparkGeneralResponse(
            id=self.id,
            msg="msg: data load",
            columns_json=columns,
            num_rows=num_rows,
        )

    # spark transforms:

    def spark_transform_filter(self, filter_sql: str):
        if session.check_load():
            session.df_current = DfUtils.filter_df(session.df_current, filter_sql)
            msg = "filter accepted"
        else:
            msg = "[Error] no dataset loaded"

        return sparkapi_session_pb2.PysparkTransformResponse(
            id=session.id,
            msg=msg,
        )


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
        session.log_(f"/preview: {req.id}, limit: {req.limit}")

        json_str_rows = session.spark_action_to_json(req.limit)
        for row in json.loads(json_str_rows):
            # time.sleep(0.5)
            row_json_obj = sparkapi_session_pb2.DatasetRowResponse(
                row_json=json.dumps(row)
            )
            yield row_json_obj

    def loadsDataset(
        self, req: sparkapi_session_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkGeneralResponse:
        session.log_(f"/load: {req.id, req.df_path, req.df_type}")

        session.spark_action_load_dataset(req.df_path, req.df_type)
        return session.get_general_spark_response()

    def filterDataset(
        self, req: sparkapi_session_pb2.FilterDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(f"/filter: {req.id, req.filter_sql}")
        return session.spark_transform_filter(req.filter_sql)

    def createSession(
        self, req: sparkapi_session_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_session_pb2.NewSessionResponse:
        session.set_id(req.id)
        session.log_(f"/createSession: {req.id}")
        session.log_(f"spark session id: {session.spark}")

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
