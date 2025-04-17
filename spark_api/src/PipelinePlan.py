from collections import deque

from pyspark.sql import SparkSession

from custom_exceptions import LoadNodeRemovalException
from Nodes import SparkNode


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

    def is_node_present(self, node: SparkNode):
        return any(n.node_id == node.node_id for n in self.nodes)

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

    def process_node(self, spark: SparkSession, node: SparkNode):
        if self.is_node_present(node):
            self.edit_node(spark, node)
        else:
            self.add_node(spark, node)

    def add_node(self, spark: SparkSession, new_node: SparkNode):
        prev_position = self.get_node_position(new_node.prev_node_id)

        if prev_position == -1:
            # append
            self.nodes.append(new_node)
        else:
            curr_position = prev_position + 1
            next_position = prev_position + 2
            # insert
            self.nodes.insert(curr_position, new_node)
            self.nodes[next_position].prev_node_id = new_node.node_id
            # rerun from next node
            self.reapply_plan(spark, next_position)

    def edit_node(self, spark: SparkSession, edited_node: SparkNode):
        # get node index
        node_position = self.get_node_position(edited_node.node_id)
        self.nodes[node_position] = edited_node
        if node_position != -1:
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
            # rerun from removed
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
