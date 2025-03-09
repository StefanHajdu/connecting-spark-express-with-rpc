import json

from pyspark.sql import DataFrame
from constants import PLAN_NODE_ROOT_ID
from custom_types import SparkNode as SN
from typing import Iterable
from abc import ABC, abstractmethod

from utils import log_plan_execution


class ClientSession:
    def __init__(self, id):
        self.id = id

    @property
    def plan(self):
        return self._plan

    @plan.setter
    def plan(self, val):
        self._plan = val

    def load_dataset(self, spark, path: str, data_type: str) -> SN:
        self._log(f"/load: {path, data_type}")
        node = LoadNode(
            session_id=self.id,
            node_id=PLAN_NODE_ROOT_ID,
            prev_node_id=None,
            operation=f"{__name__}",
            included=True,
            query="spark.read",
            path=path,
            data_type=data_type,
        )
        df = node.run_transform(spark=spark)
        node.df = df
        return node

    def load_from_session(self, input_session_plan):
        self._log(f"/loadFromSession: {input_session_plan.session_id}")
        node = LoadFromSessionNode(
            session_id=self.id,
            node_id=PLAN_NODE_ROOT_ID,
            prev_node_id=None,
            operation=f"{__name__}",
            included=True,
            query="custom.load_last_df_from_input_session",
            input_session_node_id=input_session_plan.session_id,
        )
        df = node.run_transform(input_session_plan=input_session_plan)
        node.df = df
        return node

    def create_sql_node(self, node_id, prev_node_id, query_type, included, query, query_params_json):
        self._log(f"/addNode: {node_id, prev_node_id, query}")
        node = SqlNode(
            session_id=self.id,
            node_id=node_id,
            prev_node_id=prev_node_id,
            operation="sql",
            included=included,
            query=query,
            query_type=query_type,
            query_params_json=query_params_json,
        )
        return node

    def edit_sql_node(self, node_id, query_type, query, query_params_json, included):
        self._log(f"/editNode: {node_id, query}")
        node = self.plan.get_node_by_id(node_id)
        node.edit(
            query_type=query_type,
            query=query,
            query_params_json=query_params_json,
            included=included,
        )
        return node

    def remove_node(self, spark, node_id, pause_node_flag: bool):
        self._log(f"/removeNode: {node_id, pause_node_flag}")
        self.plan.remove_node(spark, node_id, pause_node_flag)

    @log_plan_execution
    def summarize(self, node_id: str):
        self._log(f"/summarize: {node_id}")
        node = self.plan.get_node_by_id(node_id)
        return node.summarize()

    @log_plan_execution
    def preview(self, node_id: str, limit: int) -> Iterable[str]:
        self._log(f"/preview {node_id}, {limit}")
        node = self.plan.get_node_by_id(node_id)
        rows = node.preview(limit)
        for row in rows:
            yield json.dumps(row)

    def _log(self, msg):
        print(f"*** session - {self.id} *** " + msg)


class SparkNode(ABC):
    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, val: DataFrame):
        self._session_id = val

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, val: DataFrame):
        self._df = val

    @property
    def node_id(self):
        return self._node_id

    @node_id.setter
    def node_id(self, val: str):
        self._node_id = val

    @property
    def prev_node_id(self):
        return self._prev_node_id

    @prev_node_id.setter
    def prev_node_id(self, val: str):
        self._prev_node_id = val

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, val: str):
        self._operation = val

    @property
    def included(self):
        return self._included

    @included.setter
    def included(self, val: bool):
        self._included = val

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, val: bool):
        self._query = val

    def summarize(self):
        return {
            "columns": json.dumps(self.df.columns),
            "count": self.df.count(),
            "schema": self.df._jdf.schema().treeString(),
        }

    def preview(self, limit):
        return json.loads(self.df.limit(limit).toPandas().to_json(orient="records"))

    @abstractmethod
    def run_transform(self, **kwargs) -> DataFrame:
        pass


class LoadNode(SparkNode):
    def __init__(
        self,
        session_id,
        node_id,
        prev_node_id,
        operation,
        included,
        query,
        path,
        data_type,
    ):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self._operation = operation
        self._included = included
        self._query = query
        self._path = path
        self._data_type = data_type

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val: str):
        self._path = val

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, val: str):
        self._data_type = val

    def __str__(self):
        return f"node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | included: {self.included} | query: {self.query} | path: {self.path} | data_type {self.data_type}"

    def run_transform(self, **kwargs):
        spark = kwargs.get("spark")

        if self.data_type == "csv":
            return spark.read.option("delimiter", ";").option("header", True).csv(self.path)
        elif self.data_type == "json":
            return spark.read.json(self.path)


class LoadFromSessionNode(SparkNode):
    def __init__(self, session_id, node_id, prev_node_id, operation, included, query, input_session_node_id):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self._operation = operation
        self._included = included
        self._query = query
        self._input_session_node_id = input_session_node_id

    @property
    def input_session_node_id(self):
        return self._input_session_node_id

    @input_session_node_id.setter
    def input_session_node_id(self, val: str):
        self._input_session_node_id = val

    def __str__(self):
        return f"node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | included: {self.included} | query: {self.query} | input_session_node_id: {self.input_session_node_id}"

    def run_transform(self, **kwargs):
        input_session_plan = kwargs.get("input_session_plan")

        last_node = input_session_plan.get_last_spark_node()
        return last_node.df


class SqlNode(SparkNode):
    def __init__(self, session_id, node_id, prev_node_id, operation, included, query, query_type, query_params_json):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self._query_type = query_type
        self._operation = operation
        self._included = included
        self._query = query
        self._query_params_json = query_params_json

    @property
    def query_type(self):
        return self._query_type

    @query_type.setter
    def query_type(self, val: str):
        self._query_type = val

    @property
    def query_params_json(self):
        return self._query_params_json

    @query_params_json.setter
    def query_params_json(self, val: str):
        self._query_params_json = val

    def __str__(self):
        return f"node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | included: {self.included} | query: {self.query} | query_params: {self.query_params_json} | query_type: {self.query_type}"

    def run_transform(self, **kwargs):
        spark = kwargs.get("spark")
        df = kwargs.get("df")

        query_kwargs = self._get_parsed_params()
        return spark.sql(
            self.query,
            df=df,
            **query_kwargs,
        )

    def _get_parsed_params(self):
        return {}

    def edit(self, query_type, query, query_params_json, included):
        self.query_type = query_type
        self.query = query
        self.query_params_json = query_params_json
        self.included = included
