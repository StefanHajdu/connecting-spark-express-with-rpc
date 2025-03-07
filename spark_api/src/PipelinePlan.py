import sparkapi_session_pb2

from collections import deque
from typing import TypedDict
from functools import wraps

from SessionTable import SessionTable
from custom_exceptions import InvalidEditException, LoadNodeRemovalException
from ClientSession import SparkNode


class DataframeSummary(TypedDict):
    columns: str
    count: int
    schema: str


class SessionPlanner:
    def __init__(self, session_id: str, root_node: SparkNode):
        self.session_id = session_id
        self.nodes = deque([root_node])

    def get_node_by_id(self, node_id: str) -> SparkNode:
        idx = self._find_node_by_id(node_id)
        return self.nodes[idx]

    def get_last_spark_node(self) -> SparkNode:
        idx = -1
        while not isinstance(self.nodes[idx], SparkNode):
            idx -= 1
        return self.nodes[idx]

    def add_sql_to_nodes(self, node):
        original_len = len(self.nodes)
        insert_to_idx = self._find_position_to_insert(node)
        self.nodes.insert(insert_to_idx, node)
        if not insert_to_idx >= original_len:
            self.nodes[insert_to_idx + 1]["previous_node_id"] = node["node_id"]

    def _find_position_to_insert(self, new_node):
        for idx, node in enumerate(self.nodes):
            if node["node_id"] == new_node["previous_node_id"]:
                return idx + 1
        return -1

    def edit_sql_in_nodes(self, node):
        id_to_edit = self._find_node_by_id(node["node_id"])
        if id_to_edit < 0:
            raise InvalidEditException()
        self.nodes[id_to_edit]["query_type"] = node["query_type"]
        self.nodes[id_to_edit]["query"] = node["query"]
        self.nodes[id_to_edit]["query_params_json"] = node["query_params_json"]

        if node["include_sql"] and not self.nodes[id_to_edit]["include_sql"] and id_to_edit < len(self.nodes) - 1:
            self.nodes[id_to_edit + 1]["previous_node_id"] = node["node_id"]

        self.nodes[id_to_edit]["include_sql"] = node["include_sql"]

    def remove_sql_from_nodes(self, node_id: str, temp: bool):
        to_del = self._find_node_by_id(node_id)
        if to_del < 0:
            raise InvalidEditException()
        elif to_del == 0:
            raise LoadNodeRemovalException()
        elif not to_del == len(self.nodes) - 1:
            self.nodes[to_del + 1]["previous_node_id"] = self.nodes[to_del - 1]["node_id"]
        self._delete_node(to_del, temp)

    def _find_node_by_id(self, node_id: str):
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                return idx
        return -1

    def _delete_node(self, idx: int, temp: bool):
        if temp:
            self.nodes[idx]["include_sql"] = False
        else:
            del self.nodes[idx]


class SessionPlannerMap:
    def __init__(self, table: SessionTable):
        self.session_planners = {}
        self.session_table = table

    def add_session(self, session_id: str):
        self.session_planners.update({session_id: None})

    def get_session_plan(self, session_id: str):
        return self.session_planners[session_id]

    def update_session_plan(self, session_id: str, plan: SessionPlanner):
        self.session_planners[session_id] = plan

    def spark_transformation_update(self, func):
        """Adds rest api query to session plan. Plan is defined by session id and return as binary object.
        Init propagation of the change to child sessions.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            grpc_res = func(*args, **kwargs)
            self.handle_plan_change(grpc_res.session_id)
            return grpc_res

        return wrapper

    def handle_plan_change(self, session_id: str):
        """Get session ids that use current session as input. And send new query log."""
        ids_to_notify = self._get_session_dependency(session_id)
        for id_to_notify in ids_to_notify:
            self._notify_child_session_input_change(id_to_notify)

    def _get_session_dependency(self, session_id: str):
        """Filter only session that log plan starts with `loadFromSession` and uses this session id as input."""
        ls = []
        for id, planner in self.session_planners.items():
            plan_init_point = planner.plan[0]
            if plan_init_point["op"] == "loadFromSession" and plan_init_point["input_id"] == session_id:
                ls.append(id)
        return ls

    def _notify_child_session_input_change(
        self,
        id_to_notify: str,
    ):
        _ = self.session_table.get_stub(id_to_notify).notifyMasterInputChange(
            sparkapi_session_pb2.MasterInputChangeNotificationRequest(id=id_to_notify)
        )
