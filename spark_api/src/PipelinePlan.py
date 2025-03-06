import sparkapi_session_pb2
import pickle
import json

from collections import deque
from functools import wraps
from typing import TypedDict

from SessionTable import SessionTable
from custom_exceptions import InvalidEditException, LoadNodeRemovalException
from custom_types import SparkNode


class DataframeSummary(TypedDict):
    columns: str
    count: int
    schema: str


def log_plan_execution(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"\n***PLAN TO APPLY for session: {self.session_id}***")
        for idx, step in enumerate(self.plan):
            print(f"    {idx}. {step}")
        print(f"***PLAN TO APPLY for session: {self.session_id}***\n\n")

        return func(self, *args, **kwargs)

    return wrapper


class SessionPlanner:
    def __init__(self, session_id: str, root_node: SparkNode):
        self.session_id = session_id
        self.plan = deque([root_node])

    def add_sql_to_plan(self, node: SparkNode):
        original_len = len(self.plan)
        insert_to_idx = self._find_position_to_insert(node)
        self.plan.insert(insert_to_idx, node)
        if not insert_to_idx >= original_len:
            self.plan[insert_to_idx + 1]["previous_node_id"] = node["node_id"]

    def _find_position_to_insert(self, new_node: SparkNode):
        for idx, node in enumerate(self.plan):
            if node["node_id"] == new_node["previous_node_id"]:
                return idx + 1
        return -1

    def edit_sql_in_plan(self, node: SparkNode):
        id_to_edit = self._find_node_by_id(node["node_id"])
        if id_to_edit < 0:
            raise InvalidEditException()
        self.plan[id_to_edit]["query_type"] = node["query_type"]
        self.plan[id_to_edit]["query"] = node["query"]
        self.plan[id_to_edit]["query_params_json"] = node["query_params_json"]

        if node["include_sql"] and not self.plan[id_to_edit]["include_sql"] and id_to_edit < len(self.plan) - 1:
            self.plan[id_to_edit + 1]["previous_node_id"] = node["node_id"]

        self.plan[id_to_edit]["include_sql"] = node["include_sql"]

    def remove_sql_from_plan(self, node_id: str, temp: bool):
        to_del = self._find_node_by_id(node_id)
        if to_del < 0:
            raise InvalidEditException()
        elif to_del == 0:
            raise LoadNodeRemovalException()
        elif not to_del == len(self.plan) - 1:
            self.plan[to_del + 1]["previous_node_id"] = self.plan[to_del - 1]["node_id"]
        self._delete_node(to_del, temp)

    @log_plan_execution
    def summarize_node(self, node_id: str) -> DataframeSummary:
        node = self._get_node_by_id(node_id)
        df = node["df"]
        return {"columns": json.dumps(df.columns), "count": df.count(), "schema": df._jdf.schema().treeString()}

    @log_plan_execution
    def preview_node(self, node_id: str, limit: int) -> list[str]:
        node = self._get_node_by_id(node_id)
        df = node["df"]
        return json.loads(df.limit(limit).toPandas().to_json(orient="records"))

    def _get_node_by_id(self, node_id: str):
        idx = self._find_node_by_id(node_id)
        return self.plan[idx]

    def _find_node_by_id(self, node_id: str):
        for idx, node in enumerate(self.plan):
            if node["node_id"] == node_id:
                return idx
        return -1

    def _delete_node(self, idx: int, temp: bool):
        if temp:
            self.plan[idx]["include_sql"] = False
        else:
            del self.plan[idx]


class SessionPlannerMap:
    def __init__(self, table: SessionTable):
        self.session_planners = {}
        self.session_table = table

    def add_session(self, session_id: str):
        self.session_planners.update({session_id: None})

    def get_planner_pickled(self, session_id: str) -> bytes:
        return pickle.dumps(self.session_planners.get(session_id))

    def overwrite_plan(self, session_id: str, planner: SessionPlanner | bytes):
        if isinstance(planner, SessionPlanner):
            self.session_planners[session_id] = planner
        else:
            self.session_planners[session_id] = pickle.loads(planner)

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
