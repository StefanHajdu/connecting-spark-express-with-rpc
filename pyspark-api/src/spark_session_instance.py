import grpc
import os
import json
import pickle

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

from PipelinePlan import SessionPlanner

BASE_SESSION_PORT = 50051
PLAN_ROOT_ID = "0000-0000-0000"


class SqlUtils:
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
        param_name = params_json
        if param_name == "df":
            params_named[param_name] = session.df_current
        return params_named


class SparkApiSession:
    def __init__(self, pid, spark):
        self.pid = pid
        self.spark = spark
        self.df_current = None

    # setters:

    def set_id(self, id):
        self.id = id

    # utilities:

    def check_load(self):
        return True if self.df_current else False

    def log_(self, msg):
        print(f"    [child_session-{self.id}] " + msg)

    # spark actions:

    def spark_action_load_dataset(self, path, df_type, to_cache: bool = False):
        self.df_current = self.spark_transform_load_by_path(self.spark, path, df_type)

        if to_cache:
            self.df_current.cache()

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
            session_id=self.id,
            msg=msg,
            columns_json=columns,
            num_rows=num_rows,
            schema_tree=schema_str,
        )

    def spark_action_summarize(self):
        # print("\n---EXPLAIN")
        # session.df_current.explain()
        # print("---EXPLAIN\n")

        cols = json.dumps(self.df_current.columns)
        num_rows = self.df_current.count()
        schema_str = self.df_current._jdf.schema().treeString()
        return cols, num_rows, schema_str

    # spark transforms:

    def spark_transform_load_by_path(self, spark, path: str, dataset_type: str):
        if dataset_type == "csv":
            return spark.read.option("delimiter", ";").option("header", True).csv(path)
        elif dataset_type == "json":
            return spark.read.json(path)

    def spark_transform_sql(self, query: str, query_params_json: str):
        session.df_current = SqlUtils.execute_sql(spark, query, query_params_json)


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
    def __init__(self):
        self._rebuild_status = False

    @property
    def rebuild_status(self):
        return self._rebuild_status

    @rebuild_status.setter
    def rebuild_status(self, val: bool):
        self._rebuild_status = val

    def createSession(
        self, req: sparkapi_session_pb2.NewSessionRequest, unused_context
    ) -> sparkapi_session_pb2.NewSessionResponse:
        session.set_id(req.id)
        session.log_(f"/createSession: {req.id}")
        return sparkapi_session_pb2.NewSessionResponse(
            id=f"{session.id}",
            session_server_pid=f"{session.pid}",
            msg="session created",
        )

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
        session.log_(f"/summarize: {req.session_id, req.node_id}")
        self._run_plan(req.session_id, req.planner, last_node_id=req.node_id)
        return session.get_general_spark_response(msg="data available")

    def rebuildSession(
        self, req: sparkapi_session_pb2.RebuildRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(f"/rebuildSession: {req.session_id}")
        self._run_plan(req.session_id, req.planner)
        return sparkapi_session_pb2.PysparkTransformResponse(
            session_id=session.id,
            msg="plan re-applied, to see changes run action /summarize",
        )

    def _run_plan(self, session_id, planner: bytes, last_node_id=None):
        session_planner: SessionPlanner = pickle.loads(planner)
        session_planner.pretty_print(session_id)
        self._apply_plan_on_session(
            session_planner, sql_only=False, last_node_id=last_node_id
        )
        self.rebuild_status = False

    def loadsDataset(
        self, req: sparkapi_session_pb2.NewDatasetRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkGeneralResponse:
        session.log_(f"/load: {req.session_id, req.df_path, req.df_type}")
        session.spark_action_load_dataset(req.df_path, req.df_type)
        return session.get_general_spark_response(msg="msg: data loaded")

    def loadFromSession(
        self, req: sparkapi_session_pb2.DatasetFromSessionRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(f"/loadFromSession: {req.id, req.input_id}")
        planner = self._get_parent_session_plan(req.input_id)
        self._apply_plan_on_session(planner, sql_only=False)
        return sparkapi_session_pb2.PysparkTransformResponse(
            session_id=session.id,
            msg="plan traversed and loaded to session input",
        )

    def _get_parent_session_plan(self, session_id: str):
        res = stub.getParentSessionPlan(sparkapi_pb2.PlanRequest(id=session_id))
        return pickle.loads(res.planner)

    def notifyMasterInputChange(
        self,
        req: sparkapi_session_pb2.MasterInputChangeNotificationRequest,
        unused_context,
    ) -> sparkapi_session_pb2.MasterInputChangeNotificationResponse:
        session.log_(f"/notifyMasterInputChange: {req.id}")
        self.rebuild_status = True
        return sparkapi_session_pb2.MasterInputChangeNotificationResponse(
            id=req.id, verification=True
        )

    def getRebuildStatus(
        self, req: sparkapi_session_pb2.RebuildStatusRequest, unused_context
    ) -> sparkapi_session_pb2.RebuildStatusResponse:
        session.log_(f"/getRebuildStatus: {req.id}")
        return sparkapi_session_pb2.RebuildStatusResponse(
            id=req.id, rebuild_status=self.rebuild_status
        )

    def addSql(
        self, req: sparkapi_session_pb2.SqlRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(f"/addSql: {req.session_id, req.query, req.previous_node_id:}")
        session_planner: SessionPlanner = pickle.loads(req.planner)
        session_planner.add_sql_to_plan(
            {
                "node_id": req.node_id,
                "previous_node_id": req.previous_node_id,
                "op": "sql",
                "query_type": req.query_type,
                "query": req.query,
                "query_params_json": req.query_params_json,
            }
        )
        return sparkapi_session_pb2.PysparkTransformSqlResponse(
            session_id=session.id,
            msg="sql added",
            planner=pickle.dumps(session_planner),
        )

    def editSql(
        self, req: sparkapi_session_pb2.SqlRequest, unused_context
    ) -> sparkapi_session_pb2.PysparkTransformResponse:
        session.log_(f"/addSql: {req.session_id, req.query, req.previous_node_id:}")
        session_planner: SessionPlanner = pickle.loads(req.planner)
        session_planner.edit_sql_in_plan(
            {
                "node_id": req.node_id,
                "query_type": req.query_type,
                "query": req.query,
                "query_params_json": req.query_params_json,
            }
        )
        return sparkapi_session_pb2.PysparkTransformSqlResponse(
            session_id=session.id,
            msg=f"sql: {req.node_id} edited",
            planner=pickle.dumps(session_planner),
        )

    def _apply_plan_on_session(
        self, planner: SessionPlanner, sql_only: bool, last_node_id: str = None
    ):
        for current_node in planner.plan:
            op = current_node.get("op")

            # excution switch
            if op == "load" and not sql_only:
                session.spark_action_load_dataset(
                    current_node.get("df_path"),
                    current_node.get("df_type"),
                    to_cache=False,
                )
            elif op == "loadFromSession" and not sql_only:
                planner = self._get_parent_session_plan(current_node.get("input_id"))
                self._apply_plan_on_session(planner, sql_only=False)
            elif op == "sql":
                session.spark_transform_sql(
                    current_node.get("query"),
                    current_node.get("query_params_json"),
                )

            # stop condition
            if current_node.get("node_id") == last_node_id:
                break


def session_serve(port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_SparkApiSessionServicer_to_server(SparkApiSessionServicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    print(f"Child session server is starting on {port}...")
    server.start()
    server.wait_for_termination()
