import json
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame
from sparkapi_pb2 import AddColumnExpression


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
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | query: {self.query} | path: {self.path} | data_type {self.data_type}'  # noqa: E501

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
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | operation: {self.operation} | query: {self.query} | parent_session: {self.parent_session_plan.session_id}'  # noqa: E501

    def run_transform(self, **kwargs):
        last_node = self.parent_session_plan.get_last_spark_node()
        return last_node.df


class SqlNode(SparkNode):
    def __str__(self):
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | query: {self.query}'

    @property
    @abstractmethod
    def query_template(self) -> str:
        pass

    @property
    @abstractmethod
    def query(self) -> str:
        pass

    @abstractmethod
    def edit(self):
        pass

    def run_transform(self, **kwargs):
        spark = kwargs.get('spark')
        df = kwargs.get('df')

        return spark.sql(
            self.query,
            df=df,
        )


class FilterNode(SqlNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, expressions: list[str], matching: str = 'and'):
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.expressions = expressions
        self.matching = matching

    @property
    def query_template(self) -> str:
        return 'select * from {df} where'

    @property
    def query(self) -> str:
        return ' '.join([self.query_template, f' {self.matching.strip()} '.join(self.expressions)]).replace('\\"', '')

    def edit(self, expressions: list[str], matching: str):
        self.expressions = expressions
        self.matching = matching


class AddColumnNode(SqlNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, expressions: list[AddColumnExpression]):
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.expressions = expressions

    @property
    def query_template(self) -> str:
        return 'select *, {expressions} from {df}'

    @property
    def query(self) -> str:
        return self.query_template.format(
            **{
                'expressions': ', '.join([' as '.join((obj.expression, obj.col_name)) for obj in self.expressions]),
                'df': '{df}',
            }
        )

    def edit(self, expressions: str):
        self.expressions = expressions
