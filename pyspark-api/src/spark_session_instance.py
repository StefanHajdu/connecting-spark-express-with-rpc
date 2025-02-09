import grpc
import os
import json

import sparkapi_session_pb2
import sparkapi_pb2_grpc
import sparkapi_pb2

from pyspark.sql import SparkSession, DataFrame
from concurrent import futures
from typing import Iterable
from sparkapi_session_pb2_grpc import (
    SparkApiSessionServicer,
    add_SparkApiSessionServicer_to_server,
)

BASE_SESSION_PORT = 50051


class DfUtils:
    @classmethod
    def eager_cache_df(cls, df):
        df.cache().count()

    @classmethod
    def cache_df(cls, df):
        df.cache()

    @classmethod
    def drop_from_cache_df(cls, df):
        df.unpersist()

    @classmethod
    def read_spark_df(cls, spark, path: str, dataset_type: str):
        if dataset_type == "csv":
            return spark.read.option("delimiter", ";").option("header", True).csv(path)
        elif dataset_type == "json":
            return spark.read.json(path)


class SqlUtils(DfUtils):
    @classmethod
    def execute_sql(
        cls, spark: SparkSession, query: str, params_json: str
    ) -> DataFrame:
        kwargs = cls.to_named_params(params_json)
        return spark.sql(
            query,
            **kwargs,
        )

    @classmethod
    def to_named_params(cls, params_json: str):
        params_named = {}
        param_names = json.loads(params_json)
        for param_name in param_names:
            if param_name == "df":
                params_named[param_name] = session.df_current
        return params_named


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

    def spark_action_load_dataset(self, path, df_type, to_cache: bool = True):
        self.df_init = self.df_current = DfUtils.read_spark_df(
            self.spark, path, df_type
        )
        if to_cache:
            DfUtils.eager_cache_df(self.df_init)
        print(f"dataset `{path}` loaded")

    def spark_action_summarize(self):
        cols = json.dumps(self.df_current.columns)
        num_rows = self.df_current.count()
        schema_str = self.df_current._jdf.schema().treeString()
        return cols, num_rows, schema_str

    def spark_action_to_json(self, limit):
        return self.df_current.limit(limit).toPandas().to_json(orient="records")

    def get_general_spark_response(self, msg):
        if session.check_load():
            columns, num_rows, schema_str = self.spark_action_summarize()
            msg = "filter accepted"
        else:
            msg = "[Error] no dataset loaded"
            num_rows = 0
            schema_str = "err"
            columns = "err"
        return sparkapi_session_pb2.PysparkGeneralResponse(
            id=self.id,
            msg=msg,
            columns_json=columns,
            num_rows=num_rows,
            schema_tree=schema_str,
        )

    # spark transforms:

    def cache_just_current(self):
        DfUtils.drop_from_cache_df(self.df_current)
        DfUtils.cache_df(self.df_current)

    def spark_transform_sql(self, query: str, params_json: str):
        if session.check_load():
            session.df_current = SqlUtils.execute_sql(spark, query, params_json)
            msg = "Query accepted"
        else:
            msg = "[Error] no dataset loaded"

        return sparkapi_session_pb2.PysparkTransformResponse(
            id=session.id,
            msg=msg,
        )


channel = grpc.insecure_channel(f"localhost:{BASE_SESSION_PORT}")
stub = sparkapi_pb2_grpc.SparkApiStub(channel)
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
            row_json_obj = sparkapi_session_pb2.DatasetRowResponse(
                row_json=json.dumps(row)
            )
            yield row_json_obj

    def summarizeDataset(
        self, req: sparkapi_session_pb2.SummarizeDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkGeneralResponse:
        session.log_(f"/summarize: {req.id}")
        # session.cache_just_current()
        return session.get_general_spark_response(msg="data available")

    def loadsDataset(
        self, req: sparkapi_session_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkGeneralResponse:
        session.log_(f"/load: {req.id, req.df_path, req.df_type}")
        session.spark_action_load_dataset(req.df_path, req.df_type)
        return session.get_general_spark_response(msg="msg: data loaded")

    def loadFromSession(
        self, req: sparkapi_session_pb2.DatasetFromSessionRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(f"/loadFromSession: {req.id, req.input_id}")
        log_plan = self._get_session_log(req.input_id)
        msg = self._load_df_from_session_log(log_plan)
        return sparkapi_session_pb2.PysparkTransformResponse(
            id=session.id,
            msg=msg,
        )

    def _load_df_from_session_log(self, log_plan: list[dict[str:str]]) -> str:
        for step in log_plan:
            op = step.get("op")
            if op == "load":
                session.spark_action_load_dataset(
                    step.get("df_path"), step.get("df_type"), to_cache=False
                )
            elif op == "sql":
                _ = session.spark_transform_sql(
                    step.get("parametrized_query"), step.get("params_json")
                )
        session.df_init = session.df_current
        DfUtils.eager_cache_df(session.df_init)
        return "load completed"

    def _get_session_log(self, session_id: str):
        res = stub.getDataframeLog(sparkapi_pb2.LogRequest(id=session_id))
        return json.loads(res.log_json)

    def runSql(
        self, req: sparkapi_session_pb2.SqlRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(
            f"/sql: {req.id, req.parametrized_query, req.query_name, req.params_json}"
        )
        return session.spark_transform_sql(req.parametrized_query, req.params_json)

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
