from pyspark.sql import SparkSession
from collections import deque

from custom_exceptions import LoadNodeRemovalException
from ClientSession import SparkNode


class SessionPlanner:
    def __init__(self, session_id: str, root_node: SparkNode):
        self.session_id = session_id
        self.nodes = deque([root_node])

    def get_node_by_id(self, node_id: str) -> SparkNode | None:
        idx = self._find_node_by_id(node_id)
        if idx is not None:
            return self.nodes[idx]

    def _find_node_by_id(self, node_id: str) -> int | None:
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                return idx

    def get_node_position(self, node_id: str):
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                break
        return -1 if idx == len(self.nodes) - 1 else idx

    def get_last_spark_node(self) -> SparkNode:
        idx = -1
        while not isinstance(self.nodes[idx], SparkNode):
            idx -= 1
        return self.nodes[idx]

    def add_node(self, spark: SparkSession, new_sql_node: SparkNode):
        # get prev node index
        prev_position = self.get_node_position(new_sql_node.prev_node_id)
        prev_node = self.nodes[prev_position]

        # get then insert new df
        new_sql_node.df = new_sql_node.run_transform(spark=spark, df=prev_node.df)

        if prev_position == -1:
            # append
            self.nodes.append(new_sql_node)
        else:
            # rerun from appended
            self.nodes.insert(prev_position + 1, new_sql_node)
            for node_id in range(prev_position + 2, len(self.nodes)):
                node = self.nodes[node_id]
                node.df = node.run_transform(spark=spark, df=self.nodes[node_id - 1].df)

    def edit_node(self, spark: SparkSession, edited_node: SparkNode):
        # get node index
        node_position = self.get_node_position(edited_node.node_id)

        edited_node.df = edited_node.run_transform(spark=spark, df=self.nodes[node_position - 1].df)
        self.nodes[node_position] = edited_node

        if not node_position == -1:
            # rerun from edited
            self.reapply_plan(spark, node_position + 1)

    def remove_node(self, spark: SparkSession, node_id: str):
        del_position = self.get_node_position(node_id)
        if del_position == 0:
            raise LoadNodeRemovalException()
        elif del_position == -1:
            self._delete_node(del_position)
        else:
            self.nodes[del_position + 1].prev_node_id = self.nodes[del_position - 1].node_id
            self._delete_node(del_position)
            self.reapply_plan(spark, del_position)

    def _delete_node(self, position: int):
        del self.nodes[position]

    def reapply_plan(self, spark: SparkSession, start: int):
        for node_position in range(start, len(self.nodes)):
            node = self.nodes[node_position]
            node.df = node.run_transform(
                spark=spark,
                df=self.nodes[node_position - 1].df,
            )


class SessionPlannerMap:
    def __init__(self, table):
        self.session_planners = {}
        self.session_table = table

    def add_session(self, session_id: str):
        self.session_planners.update({session_id: None})

    def get_session_plan(self, session_id: str):
        return self.session_planners[session_id]

    def update_session_plan(self, session_id: str, plan: SessionPlanner):
        self.session_planners[session_id] = plan
