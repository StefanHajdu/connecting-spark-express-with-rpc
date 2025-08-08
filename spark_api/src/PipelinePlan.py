from __future__ import annotations

from collections import deque

import sparkapi_pb2
from exceptions import EmptyException, InvalidRemovalException, LoadNodeRemovalException, NodeMissingException
from pyspark.errors import PySparkException
from pyspark.sql import SparkSession

import Nodes


class SessionPlanner:
    def __init__(self, session_id: str, root_node: Nodes.SparkNode):
        self.session_id = session_id
        self.nodes = deque([root_node])

    def get_node_by_id(self, node_id: str) -> Nodes.SparkNode:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise NodeMissingException()

    def get_last_spark_node(self) -> Nodes.SparkNode:
        idx = -1
        while not isinstance(self.nodes[idx], Nodes.SparkNode):
            idx -= 1
        return self.nodes[idx]

    def insert_node(self, spark: SparkSession, node: Nodes.SparkNode) -> list[sparkapi_pb2.SparkTransformResponse]:
        if self.node_present_in_plan(node):
            return self.edit_node(spark, node)
        else:
            return self.append_node(spark, node)

    def node_present_in_plan(self, node: Nodes.SparkNode) -> bool:
        return any(n.node_id == node.node_id for n in self.nodes)

    def edit_node(self, spark: SparkSession, edited_node: Nodes.SparkNode) -> list[sparkapi_pb2.SparkTransformResponse]:
        # get node index
        node_position = self.get_node_index(edited_node.node_id)
        self.nodes[node_position] = edited_node

        return self.update_plan(spark, edited_node)

    def append_node(self, spark: SparkSession, new_node: Nodes.SparkNode) -> list[sparkapi_pb2.SparkTransformResponse]:
        prev_position = self.get_node_index(new_node.prev_node_id)
        if self._is_position_last(prev_position):
            # append
            self.nodes.append(new_node)
        else:
            # insert
            curr_position = prev_position + 1
            next_position = prev_position + 2
            self.nodes.insert(curr_position, new_node)
            self.nodes[next_position].prev_node_id = new_node.node_id

        return self.update_plan(spark, new_node)

    def remove_node(self, spark: SparkSession, node_id: str) -> list[sparkapi_pb2.SparkTransformResponse]:
        del_position = self.get_node_index(node_id)
        if del_position == 0:
            raise LoadNodeRemovalException()
        elif self._is_position_last(del_position):
            self._delete_node(del_position)
            return self.update_plan(spark, self.nodes[del_position - 1])
        else:
            if not isinstance(ex := self.is_removal_safe(spark, del_position), InvalidRemovalException):
                self.nodes[del_position + 1].prev_node_id = self.nodes[del_position - 1].node_id
                self._delete_node(del_position)
                return self.update_plan(spark, self.nodes[del_position])
            else:
                raise ex

    def get_node_index(self, node_id: str) -> int:
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                return idx
        raise NodeMissingException()

    def _is_position_last(self, node_position: int) -> bool:
        return node_position == len(self.nodes) - 1

    def is_removal_safe(self, spark: SparkSession, to_remove_idx: int) -> Exception:
        node_positions = [to_remove_idx - 1] + list(range(to_remove_idx + 1, len(self.nodes)))
        try:
            for idx in range(1, len(node_positions)):
                node = self.nodes[node_positions[idx]]
                node.df = node.run_transform(spark=spark, df=self.nodes[node_positions[idx - 1]].df)
            return EmptyException()
        except PySparkException as ex:
            msg = f'Error: {ex.getErrorClass()}, params: {ex.getMessageParameters()}, recorded on node: {self.nodes[node_positions[idx]].node_id}'  # noqa
            return InvalidRemovalException(msg)

    def _delete_node(self, position: int):
        del self.nodes[position]

    def update_plan(self, spark: SparkSession, starting_node: Nodes.SparkNode) -> list[sparkapi_pb2.SparkTransformResponse]:
        node_index = self.get_node_index(starting_node.node_id)

        recorded_spark_transforms = []
        for node_position in range(node_index, len(self.nodes)):
            node = self.nodes[node_position]
            prev_node = self.nodes[node_position - 1]

            try:
                node.df = node.run_transform(spark=spark, df=prev_node.df)
                recorded_spark_transforms.append(
                    sparkapi_pb2.SparkTransformResponse(
                        session_id='',
                        node_id=node.node_id,
                        invalid_state=sparkapi_pb2.InvalidState(active=False, error_msg=''),
                        columns=node.columns,
                    )
                )
            except PySparkException as ex:
                # invalidate rest of nodes
                for position_of_invalid in range(node_position, len(self.nodes)):
                    node = self.nodes[position_of_invalid]
                    recorded_spark_transforms.append(
                        sparkapi_pb2.SparkTransformResponse(
                            session_id='',
                            node_id=node.node_id,
                            invalid_state=sparkapi_pb2.InvalidState(
                                active=True, error_msg=f'{ex.getErrorClass()} with {ex.getMessageParameters()} in node: {node.node_id}'
                            ),
                            columns=node.columns,
                        )
                    )
                    break

        return recorded_spark_transforms
