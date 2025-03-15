import json
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame


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
    def query(self):
        return self._query

    @query.setter
    def query(self, val: bool):
        self._query = val

    def summarize(self):
        return {
            'columns': json.dumps(self.df.columns),
            'count': self.df.count(),
            'schema': self.df._jdf.schema().treeString(),
        }

    def preview(self, limit):
        for item in self.df.take(limit):
            yield item.asDict()

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
        query,
        path,
        data_type,
    ):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self._operation = operation
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
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | query: {self.query} | path: {self.path} | data_type {self.data_type}'

    def run_transform(self, **kwargs):
        spark = kwargs.get('spark')

        if self.data_type == 'csv':
            return spark.read.option('delimiter', ';').option('header', True).csv(self.path)
        elif self.data_type == 'json':
            return spark.read.json(self.path)


class LoadFromSessionNode(SparkNode):
    def __init__(self, session_id, node_id, prev_node_id, operation, query, parent_session_plan):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self._operation = operation
        self._query = query
        self._parent_session_plan = parent_session_plan

    @property
    def parent_session_plan(self):
        return self._parent_session_plan

    @parent_session_plan.setter
    def parent_session_plan(self, val: str):
        self._parent_session_plan = val

    def __str__(self):
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | query: {self.query} | parent_session: {self.parent_session_plan.session_id}'

    def run_transform(self, **kwargs):
        last_node = self.parent_session_plan.get_last_spark_node()
        return last_node.df


class SqlNode(SparkNode):
    def __init__(self, session_id, node_id, prev_node_id, operation, query, query_type, query_params_json):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self._query_type = query_type
        self._operation = operation
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
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | query: {self.query} | query_params: {self.query_params_json} | query_type: {self.query_type}'

    def run_transform(self, **kwargs):
        spark = kwargs.get('spark')
        df = kwargs.get('df')

        query_kwargs = self._get_parsed_params()
        return spark.sql(
            self.query,
            df=df,
            **query_kwargs,
        )

    def _get_parsed_params(self):
        return {}

    def edit(self, query_type, query, query_params_json):
        self.query_type = query_type
        self.query = query
        self.query_params_json = query_params_json
