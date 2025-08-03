from __future__ import annotations

import Nodes
import PipelinePlan
from api_logging import log_plan_execution
from misc_types import SparkActionMetadata
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
    def __init__(self, id, name):
        self.id = id
        self.name = name
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
    def plan(self, val: PipelinePlan.SessionPlanner):
        self._plan = val

    def notify_transformation_change(self):
        for child_session in self.child_sessions:
            child_session.update_status.trigger('Plan changed, operation add/edit/remove applied')

    def submit_node(self, node_class: str, **kwargs):
        self._log(f'/addNode/{node_class}')
        node_constructor = getattr(Nodes, node_class)
        node = node_constructor(**kwargs)
        return node

    def remove_node(self, node):
        self._log(f'/removeNode: {node.node_id}')
        if isinstance(node, Nodes.TransformNode):
            self.notify_transformation_change()
        self.plan.remove_node(spark, node.node_id)

    @log_plan_execution('/rebuildSession')
    def rebuild(self):
        self.plan.sync_dataframes(spark, start=0)
        self.update_status.reset()

    @log_plan_execution('/summarize')
    def summarize(self, node_id: str) -> SparkActionMetadata:
        self.plan.sync_dataframes(spark, start=1)
        node = self.plan.get_node_by_id(node_id)
        return node.summarize()

    @log_plan_execution('/preview')
    def preview(self, node: Nodes.SparkNode, limit: int):
        self.plan.sync_dataframes(spark, start=1)
        if isinstance(node, Nodes.VisualizationNode):
            prev_df = self.plan.get_node_by_id(node.prev_node_id).df
            return node.preview(limit=limit, prev_df=prev_df)
        else:
            return node.preview(limit=limit)

    def get_session_status(self):
        self._log(f'/getSessionStatus: {self.id}')
        return self.update_status.__dict__

    def _log(self, msg):
        print(f'*** session - {self.id} *** ' + msg)
