import json
from collections.abc import Iterable
from functools import wraps

import Nodes
from custom_exceptions import NodeMissingException
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

    def notify_transformation_change(self):
        for child_session in self.child_sessions:
            child_session.update_status.trigger('Plan changed, operation add/edit/remove applied')

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

    def add_node(self, node_class: str, **kwargs):
        self._log(f'/addNode/{node_class}')
        node_constructor = getattr(Nodes, node_class)
        node = node_constructor(**kwargs)
        return node

    def edit_node(self, node_id: str, **kwargs):
        node = self.plan.get_node_by_id(node_id)
        self._log(f'/editNode/{node.__class__.__name__}: {node_id}')
        prev_df = self.plan.get_node_by_id(node.prev_node_id).df
        node.edit(prev_df=prev_df, **kwargs)
        self.plan.edit_node(spark, node)

    def remove_node(self, node):
        self._log(f'/removeNode: {node.node_id}')
        if isinstance(node, Nodes.TransformNode):
            self.notify_transformation_change()
        self.plan.remove_node(spark, node.node_id)

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
