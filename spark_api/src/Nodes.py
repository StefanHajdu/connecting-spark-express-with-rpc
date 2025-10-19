from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any

import sparkapi_pb2
from constants import PLAN_NODE_ROOT_ID
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from pyspark.sql import DataFrame

import NodeExtensions
import PipelinePlan
from misc_types import SparkActionMetadata
from NodeQuery import node_query_factory
from spark_session_init import spark
from utils import load_data_for_spark


class SparkNode(ABC):
    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, val: str):
        self._session_id = val

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, val: DataFrame):
        self._df = val

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val: bool):
        self._active = val

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
    def columns(self):
        types = []
        for field in json.loads(self.df.schema.json()).get('fields', []):
            field_type = field.get('type', '')
            if isinstance(field_type, dict):
                field_type = f'{field_type["type"]}<{field_type["elementType"]}>'
            types.append(sparkapi_pb2.Column(name=field.get('name', ''), dtype=field_type))

        return types

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, val: str):
        self._query = val

    @property
    def node_input_submitted(self):
        return self._node_input_submitted

    @node_input_submitted.setter
    def node_input_submitted(self, val: bool):
        self._node_input_submitted = val

    @property
    def user_input(self):
        return self._user_input

    @user_input.setter
    def user_input(self, val: Any):
        self._user_input = val

    @property
    def query_kwargs(self) -> dict:
        return self._query_kwargs

    @query_kwargs.setter
    def query_kwargs(self, val: dict):
        self._query_kwargs = val

    def summarize(self) -> SparkActionMetadata:
        return {
            'columns': json.dumps(self.df.columns),
            'count': self.df.count(),
            'schema': self.df.schema.json(),
        }

    @abstractmethod
    def preview(self, **kwargs) -> str:
        pass

    def run_transform(self, **kwargs) -> DataFrame:
        spark = kwargs.pop('spark')

        node_query_state = node_query_factory(self.active, self.node_input_submitted, self.query)
        query_kwargs_complete = {**kwargs, **self.query_kwargs}

        df_result = spark.sql(
            node_query_state.get_query(),
            **query_kwargs_complete,
        )
        return df_result


class TransformNode(SparkNode):
    def __init__(self):
        self._active = True

    def __str__(self):
        return f'[Transform - {self.__class__.__name__}] -> node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | query: {self.query}'

    @property
    @abstractmethod
    def query_template(self) -> str:
        pass

    @property
    @abstractmethod
    def query(self) -> str:
        pass

    @property
    @abstractmethod
    def node_input_submitted(self) -> bool:
        pass

    def user_input_to_json(self) -> str:
        if isinstance(self.user_input, Message):
            return json.dumps(MessageToDict(self.user_input))
        elif isinstance(self.user_input, list):
            return json.dumps([MessageToDict(i) for i in self.user_input])
        else:
            return ''

    def preview(self, limit: int) -> str:
        df_pandas = self.df.limit(limit).toPandas()
        # orient='values' translate easiest to html table
        json_buffer = df_pandas.to_json(orient='values', force_ascii=False, date_format='iso')
        return (
            # concat df values and schema to valid json
            '{"data":'
            + json_buffer
            + ',"columns":'
            + json.dumps([{'name': field['name'], 'type': field['type']} for field in json.loads(self.df.schema.json())['fields']])
            + '}'
        )


class LoadNode(TransformNode):
    def __init__(self, session_id: str, user_input: Any):
        super().__init__()
        self._session_id = session_id
        self._node_id = PLAN_NODE_ROOT_ID
        self._prev_node_id = None
        self._user_input = user_input
        self.df = self.run_transform()

    @property
    def node_input_submitted(self) -> bool:
        return self.user_input is not None

    @property
    def query_template(self) -> str:
        return ''

    @property
    def query(self) -> str:
        return ''

    def __str__(self):
        return f'[{self.__class__.__name__}] -> session_id: {self.node_id} | {self.user_input_to_json()}'

    def run_transform(self, **kwargs):
        return load_data_for_spark(input_metadata=self.user_input)


class LoadFromSessionNode(TransformNode):
    def __init__(self, session_id: str, parent_session_plan: PipelinePlan.SessionPlanner):
        super().__init__()
        self._session_id = session_id
        self._node_id = PLAN_NODE_ROOT_ID
        self._prev_node_id = None
        self._parent_session_plan = parent_session_plan
        self.df = self.run_transform()

    @property
    def node_input_submitted(self) -> bool:
        return self._parent_session_plan is not None

    @property
    def query_template(self) -> str:
        return ''

    @property
    def query(self) -> str:
        return ''

    @property
    def parent_session_plan(self):
        return self._parent_session_plan

    @parent_session_plan.setter
    def parent_session_plan(self, val: PipelinePlan.SessionPlanner):
        self._parent_session_plan = val

    def __str__(self):
        return f'[Load - {self.__class__.__name__}] -> node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | parent_session: {self.parent_session_plan.session_id}'  # noqa: E501

    def run_transform(self, **kwargs):
        last_node = self.parent_session_plan.get_last_spark_node()
        return last_node.df


class FilterNode(TransformNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, expressions: list[str], matching: str, prev_df: DataFrame):
        super().__init__()
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.expressions = expressions
        self.matching = matching
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def node_input_submitted(self) -> bool:
        return self.expressions is not None and self.matching is not None

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


class AddColumnNode(TransformNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, user_input: list[sparkapi_pb2.AddColumnExpression], prev_df: DataFrame):
        super().__init__()
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.user_input = user_input
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def node_input_submitted(self) -> bool:
        return len(self.user_input) > 0

    @property
    def query_template(self) -> str:
        return 'select *, {expressions} from {df}'

    @property
    def query(self) -> str:
        expressions = ', '.join([expr.expression.compiled for expr in self.user_input])
        return self.query_template.format(expressions=expressions, df='{df}')

    @property
    def query_kwargs(self) -> dict:
        return {}


class JoinNode(TransformNode):
    def __init__(
        self,
        session_id: str,
        node_id: str,
        prev_node_id: str,
        input_metadata: sparkapi_pb2.CsvInput | sparkapi_pb2.JsonInput | sparkapi_pb2.ParquetInput | sparkapi_pb2.SessionInput,
        join_params: sparkapi_pb2.JoinParams,
        prev_df: DataFrame,
    ):
        super().__init__()
        self.session_id = session_id
        self.node_id = node_id
        self.prev_node_id = prev_node_id
        self.other_df = NodeExtensions.OtherDataframe(input_metadata)
        self.join_params = MessageToDict(join_params)
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def node_input_submitted(self) -> bool:
        return self.join_params is not None

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
        if len(self.join_params) > 0:
            columns_to_add = [
                ' as '.join(('{other_df}.' + col_name, self.join_params.get('prefixForAddedColumns', '') + col_name))
                for col_name in self.join_params.get('columnsToAdd', [])
            ]
            columns_to_keep = ['{df}.' + col_name for col_name in self.join_params.get('columnsToKeep', [])]
            join_criteria = f' {self.join_params.get("criteriaMatching", "").strip()} '.join(self.join_params.get('joinCriteria', []))
            return self.query_template.format(
                columns=', '.join(columns_to_keep + columns_to_add),
                df='{df}',
                join_relation=self.join_params.get('joinRelation', ''),
                other_df='{other_df}',
                join_criteria='on ' + join_criteria if join_criteria else '',
            )
        else:
            return self.other_df.query


class VisualizationNode(SparkNode):
    def __init__(self):
        self._active = True

    def __str__(self):
        return f'[Visualization - {self.__class__.__name__}] -> node_id: {self.node_id} | prev_node_id: {self.prev_node_id} | query: {self.query}'  # noqa

    @property
    def query(self) -> str:
        return 'select * from {df}'

    @property
    def query_kwargs(self) -> dict:
        return {}

    @property
    @abstractmethod
    def node_input_submitted(self) -> bool:
        pass

    @property
    @abstractmethod
    def visualization_query(self) -> str:
        pass

    @property
    @abstractmethod
    def visualization_query_template(self) -> str:
        pass

    @property
    def visualization_df(self):
        return self._visualization_df

    @visualization_df.setter
    def visualization_df(self, val: DataFrame):
        self._visualization_df = val

    def preview(self, limit: int, prev_df: DataFrame) -> str:
        visualization_df = spark.sql(self.visualization_query, df=prev_df)
        df_subset = visualization_df.limit(limit).toPandas()
        json_buffer = df_subset.to_json(orient='values', force_ascii=False, date_format='iso')
        return (
            # concat df values and schema to valid json
            '{"data":'
            + json_buffer
            + ',"columns":'
            + json.dumps([{'name': field['name'], 'type': field['type']} for field in json.loads(self.df.schema.json())['fields']])
            + '}'
        )


class TableNode(VisualizationNode):
    def __init__(self, session_id: str, node_id: str, prev_node_id: str, prev_df: DataFrame):
        super().__init__()
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def node_input_submitted(self) -> bool:
        return True

    @property
    def visualization_query(self) -> str:
        return self.visualization_query_template

    @property
    def visualization_query_template(self) -> str:
        return 'select * from {df}'


class HistogramNode(VisualizationNode):
    def __init__(
        self,
        session_id: str,
        node_id: str,
        prev_node_id: str,
        y_axis_col: str,
        order_by: str,
        sort_by: str,
        expression: str,
        prev_df: DataFrame,
    ):
        super().__init__()
        self._session_id = session_id
        self._node_id = node_id
        self._prev_node_id = prev_node_id
        self.y_axis_col = y_axis_col
        self.order_by = order_by
        self.sort_by = sort_by
        self.expression = expression
        self.df = self.run_transform(spark=spark, df=prev_df)

    @property
    def node_input_submitted(self) -> bool:
        return self.y_axis_col is not None

    @property
    def visualization_query(self) -> str:
        return self.visualization_query_template.format(
            y_axis_col=self.y_axis_col,
            expression=self.expression,
            df='{df}',
            order_by=self.order_by,
            sort_by=self.sort_by,
        )

    @property
    def visualization_query_template(self) -> str:
        return """
            select {y_axis_col}, {expression} as agg
            from {df}
            group by {y_axis_col}
            order by {order_by} {sort_by}
        """
