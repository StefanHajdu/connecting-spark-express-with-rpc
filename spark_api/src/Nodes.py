import json
from abc import abstractmethod

from pyspark.sql import DataFrame
from sparkapi_pb2 import AddColumnExpression

from constants import PLAN_NODE_ROOT_ID
from NodeExtensions import OtherDataframe
from spark_session_init import spark
from utils import spark_read_from_path


class SparkNode:
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
            'schema': self.df.schema.json(),
        }

    def preview(self, limit):
        for item in self.df.take(limit):
            yield item.asDict()

    def run_transform(self, **kwargs) -> DataFrame:
        spark = kwargs.pop('spark')
        df_result = spark.sql(
            self.query,
            **{**kwargs, **self.query_kwargs},
        )
        return df_result


class TransformNode(SparkNode):
    def __str__(self):
        return f'[Transform] -> node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | query: {self.query}'

    @property
    @abstractmethod
    def query(self) -> str:
        pass

    @property
    @abstractmethod
    def query_template(self) -> str:
        pass

    @property
    @abstractmethod
    def query_kwargs(self) -> dict:
        pass

    @abstractmethod
    def edit(self):
        pass


class LoadNode(TransformNode):
    def __init__(self, session_id: str, path: str, data_type: str):
        self._session_id = session_id
        self._node_id = PLAN_NODE_ROOT_ID
        self._prev_node_id = None
        self._operation = 'load_dataset'
        self._query = 'spark.read'
        self._path = path
        self._data_type = data_type
        self.df = self.run_transform()

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
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | path: {self.path}'

    def run_transform(self, **kwargs):
        return spark_read_from_path(data_type=self.data_type, path=self.path)


class LoadFromSessionNode(TransformNode):
    def __init__(self, session_id: str, parent_session_plan: str):
        self._session_id = session_id
        self._node_id = PLAN_NODE_ROOT_ID
        self._prev_node_id = None
        self._operation = 'load_from_session'
        self._query = 'load_from_session'
        self._parent_session_plan = parent_session_plan
        self.df = self.run_transform()

    @property
    def parent_session_plan(self):
        return self._parent_session_plan

    @parent_session_plan.setter
    def parent_session_plan(self, val: str):
        self._parent_session_plan = val

    def __str__(self):
        return f'node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | parent_session: {self.parent_session_plan.session_id}'  # noqa: E501

    def run_transform(self, **kwargs):
        last_node = self.parent_session_plan.get_last_spark_node()
        return last_node.df


class FilterNode(TransformNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, expressions: list[str], matching: str, prev_df: DataFrame):
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.expressions = expressions
        self.matching = matching
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def query_template(self) -> str:
        return 'select * from {df} where {expressions}'

    @property
    def query(self) -> str:
        expressions = f' {self.matching.strip()} '.join(self.expressions)
        return self.query_template.format(expressions=expressions, df='{df}')

    @property
    def query_kwargs(self) -> dict:
        return {}

    def edit(self, expressions: list[str], matching: str, prev_df: DataFrame):
        self.expressions = expressions
        self.matching = matching
        self.df = self.run_transform(spark=spark, df=prev_df)


class NewColumnNode(TransformNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, expressions: list[str], prev_df: DataFrame):
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.expressions = expressions
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def query_template(self) -> str:
        return 'select *, {expressions} from {df}'

    @property
    def query(self) -> str:
        expressions = ', '.join([' as '.join((obj.expression, obj.col_name)) for obj in self.expressions])
        return self.query_template.format(expressions=expressions, df='{df}')

    @property
    def query_kwargs(self) -> dict:
        return {}

    def edit(self, expressions: str, prev_df: DataFrame):
        self.expressions = expressions
        self.df = self.run_transform(spark=spark, df=prev_df)


class JoinNode(TransformNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, input_type: str, input_pointer: str, prev_df: DataFrame):
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.other_df = OtherDataframe(input_type, input_pointer)
        self._query = None
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def query_template(self) -> str:
        return """select {columns} from {df}
            {join_relation} join
            {other_df}
            {join_criteria}"""

    @property
    def query_kwargs(self) -> dict:
        return {'other_df': self.other_df.df}

    @property
    def query(self) -> str:
        try:
            columns_to_add = [
                ' as '.join(('{other_df}.' + col_name, self.prefix_for_added_columns + col_name)) for col_name in self.columns_to_add
            ]
            columns_to_keep = ['{df}.' + col_name for col_name in self.columns_to_keep]
            join_criteria = f' {self.criteria_matching.strip()} '.join(self.join_criteria)
            return self.query_template.format(
                columns=', '.join(columns_to_keep + columns_to_add),
                df='{df}',
                join_relation=self.join_relation,
                other_df='{other_df}',
                join_criteria='on ' + join_criteria if join_criteria else '',
            )
        except Exception:
            return self.other_df.query

    def edit(
        self,
        join_relation: str,
        columns_to_keep: list[str],
        columns_to_add: list[str],
        prefix_for_added_columns: str,
        join_criteria: list[str],
        criteria_matching: str,
        prev_df: DataFrame,
    ):
        self.join_relation = join_relation
        self.columns_to_keep = columns_to_keep
        self.columns_to_add = columns_to_add
        self.prefix_for_added_columns = prefix_for_added_columns
        self.join_criteria = join_criteria
        self.criteria_matching = criteria_matching
        self.df = self.run_transform(spark=spark, df=prev_df)


class VisualizationNode(SparkNode):
    def __str__(self):
        return f'[Visualization] -> node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | query: {self.query}'

    @property
    @abstractmethod
    def query(self) -> str:
        pass

    @property
    @abstractmethod
    def query_template(self) -> str:
        pass

    @property
    @abstractmethod
    def query_kwargs(self) -> str:
        pass

    @abstractmethod
    def edit(self):
        pass


class TableNode(VisualizationNode):
    def __init__(self, session_id, node_id, prev_node_id):
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id

    @property
    def query(self) -> str:
        return self.query_template

    @property
    def query_template(self) -> str:
        return 'select * from {df}'

    @property
    def query_kwargs(self) -> dict:
        return {}

    def edit(self):
        pass
