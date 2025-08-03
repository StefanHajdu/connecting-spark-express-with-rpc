from __future__ import annotations

from collections import deque

from exceptions import EmptyException, InvalidRemovalException, LoadNodeRemovalException, NodeMissingException
from pyspark.errors import PySparkException
from pyspark.sql import SparkSession

import Nodes


class SessionPlanner:
    def __init__(self, session_id: str, root_node: Nodes.SparkNode):
        self.session_id = session_id
        self.nodes = deque([root_node])

    def get_node_by_id(self, node_id: str) -> Nodes.SparkNode:
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                return self.nodes[idx]
        raise NodeMissingException()

    def is_node_present(self, node: Nodes.SparkNode) -> bool:
        return any(n.node_id == node.node_id for n in self.nodes)

    def get_node_index(self, node_id: str) -> int:
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                return -1 if idx == len(self.nodes) - 1 else idx
        raise NodeMissingException()

    def get_last_spark_node(self) -> Nodes.SparkNode:
        idx = -1
        while not isinstance(self.nodes[idx], Nodes.SparkNode):
            idx -= 1
        return self.nodes[idx]

    def insert_node(self, spark: SparkSession, node: Nodes.SparkNode):
        if self.is_node_present(node):
            self.edit_node(spark, node)
        else:
            self.add_node(spark, node)

    def add_node(self, spark: SparkSession, new_node: Nodes.SparkNode):
        prev_position = self.get_node_index(new_node.prev_node_id)

        if prev_position == -1:
            # append
            self.nodes.append(new_node)
        else:
            curr_position = prev_position + 1
            next_position = prev_position + 2
            # insert
            self.nodes.insert(curr_position, new_node)
            self.nodes[next_position].prev_node_id = new_node.node_id

    def edit_node(self, spark: SparkSession, edited_node: Nodes.SparkNode):
        # get node index
        node_position = self.get_node_index(edited_node.node_id)
        self.nodes[node_position] = edited_node

    def remove_node(self, spark: SparkSession, node_id: str):
        del_position = self.get_node_index(node_id)
        if del_position == 0:
            raise LoadNodeRemovalException()
        elif del_position == -1:
            self._delete_node(del_position)
        else:
            if not isinstance(ex := self.is_removal_safe(spark, del_position), InvalidRemovalException):
                self.nodes[del_position + 1].prev_node_id = self.nodes[del_position - 1].node_id
                self._delete_node(del_position)
            else:
                raise ex

    def _delete_node(self, position: int):
        del self.nodes[position]

    def sync_dataframes(self, spark: SparkSession, start: int):
        for node_position in range(start, len(self.nodes)):
            node = self.nodes[node_position]
            node.df = node.run_transform(
                spark=spark,
                df=self.nodes[node_position - 1].df,
            )

    def is_removal_safe(self, spark: SparkSession, to_remove_idx: int) -> Exception:
        node_positions = [to_remove_idx - 1] + list(range(to_remove_idx + 1, len(self.nodes)))
        try:
            for idx in range(1, len(node_positions)):
                node = self.nodes[node_positions[idx]]
                node.df = node.run_transform(
                    spark=spark,
                    df=self.nodes[node_positions[idx - 1]].df,
                )
            return EmptyException()
        except PySparkException as ex:
            msg = f'Error: {ex.getErrorClass()}, params: {ex.getMessageParameters()}, recorded on node: {self.nodes[node_positions[idx]].node_id}'
            return InvalidRemovalException(msg)
