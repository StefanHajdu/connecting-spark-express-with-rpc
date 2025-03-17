import json
from collections.abc import Iterable
from functools import wraps

from sparkapi_pb2 import AddColumnExpression

from constants import PLAN_NODE_ROOT_ID
from custom_exceptions import NodeMissingException
from Nodes import AddColumnNode, FilterNode, LoadFromSessionNode, LoadNode
from spark_session_init import spark


class UpdateStatus:
    def __init__(self):
        self.rebuild_recommendation = False
        self.cause = ''

    def __repr__(self):
        return f'rebuild_recommendation: {self.rebuild_recommendation}; cause {self.cause}'

    def reset(self):
        self.rebuild_recommendation = False
        self.cause = ''

    def trigger(self, msg: str):
        self.rebuild_recommendation = True
        self.cause = msg


class ClientSession:
    def __init__(self, id):
        self.id = id
        self.child_sessions = set()
        self.update_status = UpdateStatus()

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f'session: {self.id}, status: {self.update_status}'

    def add_child_session(self, session_id):
        self.child_sessions.add(session_id)

    @property
    def plan(self):
        return self._plan

    @plan.setter
    def plan(self, val):
        self._plan = val

    def log_plan_execution(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            print(f'>>> PLAN TO APPLY for session: {self.id} >>>')
            for idx, node in enumerate(self.plan.nodes):
                print(f'    {idx}. {node}')
            print(f'>>> PLAN TO APPLY for session: {self.id} >>>\n')
            return res

        return wrapper

    def notify_plan_change(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)

            for child_session in self.child_sessions:
                child_session.update_status.trigger('Plan changed, operation add/edit/remove applied')

            return res

        return wrapper

    def load_dataset(self, path: str, data_type: str):
        self._log(f'/load: {path, data_type}')
        node = LoadNode(
            session_id=self.id,
            node_id=PLAN_NODE_ROOT_ID,
            prev_node_id=None,
            operation=f'{__name__}',
            query='spark.read',
            path=path,
            data_type=data_type,
        )
        df = node.run_transform(spark=spark)
        node.df = df
        return node

    def load_from_session(self, parent_session, parent_session_plan):
        self._log(f'/loadFromSession: {parent_session_plan.session_id}')
        node = LoadFromSessionNode(
            session_id=self.id,
            node_id=PLAN_NODE_ROOT_ID,
            prev_node_id=None,
            operation=f'{__name__}',
            query='custom.load_last_df_from_input_session',
            parent_session_plan=parent_session_plan,
        )
        parent_session.add_child_session(self)
        df = node.run_transform()
        node.df = df
        return node

    @notify_plan_change
    def add_filter_node(self, node_id: str, prev_node_id: str, expressions: list[str], matching: str):
        self._log(f'/addNode/filter: {node_id, prev_node_id}')
        new_sql_node = FilterNode(
            session_id=self.id,
            node_id=node_id,
            prev_node_id=prev_node_id,
            expressions=expressions,
            matching=matching,
        )
        self.plan.add_node(spark, new_sql_node)

    @notify_plan_change
    def edit_filter_node(self, node_id: str, expressions: list[str], matching: str):
        self._log(f'/editNode/filter: {node_id}')
        node = self.plan.get_node_by_id(node_id)
        node.edit(expressions=expressions, matching=matching)
        self.plan.edit_node(spark, node)

    @notify_plan_change
    def add_addColumn_node(self, node_id: str, prev_node_id: str, expressions: list[AddColumnExpression]):
        self._log(f'/addNode/addColumn: {node_id, prev_node_id}')
        new_sql_node = AddColumnNode(
            session_id=self.id,
            node_id=node_id,
            prev_node_id=prev_node_id,
            expressions=expressions,
        )
        self.plan.add_node(spark, new_sql_node)

    @notify_plan_change
    def edit_addColumn_node(self, node_id: str, expressions: list[AddColumnExpression]):
        self._log(f'/editNode/addColumn: {node_id}')
        node = self.plan.get_node_by_id(node_id)
        node.edit(expressions=expressions)
        self.plan.edit_node(spark, node)

    @notify_plan_change
    def remove_node(self, node_id):
        self._log(f'/removeNode: {node_id}')
        self.plan.remove_node(spark, node_id)

    @log_plan_execution
    def rebuild(self):
        self._log(f'/rebuildSession: {self.id}')
        self.plan.reapply_plan(spark, start=0)
        self.update_status.reset()

    @log_plan_execution
    def summarize(self, node_id: str):
        self._log(f'/summarize: {node_id}')
        node = self.plan.get_node_by_id(node_id)
        if node:
            return node.summarize()
        else:
            raise NodeMissingException()

    @log_plan_execution
    def preview(self, node_id: str, limit: int) -> Iterable[str]:
        self._log(f'/preview {node_id}, {limit}')
        node = self.plan.get_node_by_id(node_id)
        rows = node.preview(limit)
        for row in rows:
            yield json.dumps(row)

    def get_session_status(self):
        self._log(f'/getSessionStatus: {self.id}')
        return self.update_status.__dict__

    def _log(self, msg):
        print(f'*** session - {self.id} *** ' + msg)
