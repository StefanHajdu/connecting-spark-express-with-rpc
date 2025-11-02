from __future__ import annotations

from collections import deque

import sparkapi_pb2
from pyspark.errors import PySparkException
from pyspark.sql import SparkSession

from core import Nodes
from core.exceptions import LoadNodeRemovalException, NodeMissingException


class SessionPlanner:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.nodes = deque([])

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
        node_position = self.get_node_index(edited_node.node_id)
        self.nodes[node_position] = edited_node
        return self.refresh_plan(spark, edited_node)

    def append_node(self, spark: SparkSession, new_node: Nodes.SparkNode) -> list[sparkapi_pb2.SparkTransformResponse]:
        if isinstance(new_node, Nodes.LoadNode):
            self.nodes.append(new_node)
        else:
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
        return self.refresh_plan(spark, new_node)

    def remove_node(self, spark: SparkSession, node_id: str) -> list[sparkapi_pb2.SparkTransformResponse]:
        del_position = self.get_node_index(node_id)
        if del_position == 0:
            raise LoadNodeRemovalException()
        elif self._is_position_last(del_position):
            self._delete_node(del_position)
            return self.refresh_plan(spark, self.nodes[del_position - 1])
        else:
            self.nodes[del_position + 1].prev_node_id = self.nodes[del_position - 1].node_id
            self._delete_node(del_position)
            return self.refresh_plan(spark, self.nodes[del_position])

    def get_node_index(self, node_id: str | None) -> int:
        for idx, node in enumerate(self.nodes):
            if node.node_id == node_id:
                return idx
        raise NodeMissingException()

    def _is_position_last(self, node_position: int) -> bool:
        return node_position == len(self.nodes) - 1

    def _delete_node(self, position: int):
        del self.nodes[position]

    def refresh_plan(self, spark: SparkSession, starting_node: Nodes.SparkNode, include_user_input: bool = False) -> list[sparkapi_pb2.SparkTransformResponse]:
        node_index = self.get_node_index(starting_node.node_id)

        recorded_spark_transforms = []
        for node_position in range(node_index, len(self.nodes)):
            node = self.nodes[node_position]
            prev_node_index = node_position - 1 if node_position > 0 else 0
            prev_node = self.nodes[prev_node_index]

            try:
                node.df = node.run_transform(spark=spark, df=prev_node.df)
                recorded_spark_transforms.append(
                    sparkapi_pb2.SparkTransformResponse(
                        session_id='',
                        node_id=node.node_id,
                        prev_node_id=prev_node.node_id,
                        title=node.__class__.__name__,
                        invalid_state=sparkapi_pb2.InvalidState(active=False, error_msg=''),
                        active=node.active,
                        columns=node.columns,
                        user_input=node.user_input_to_json() if include_user_input else '',
                    )
                )
            except PySparkException as ex:
                # invalidate rest of nodes
                for position_of_invalid in range(node_position, len(self.nodes)):
                    node = self.nodes[position_of_invalid]
                    prev_node_index = position_of_invalid - 1 if position_of_invalid > 0 else 0
                    prev_node = self.nodes[prev_node_index]
                    recorded_spark_transforms.append(
                        sparkapi_pb2.SparkTransformResponse(
                            session_id='',
                            node_id=node.node_id,
                            prev_node_id=prev_node.node_id,
                            title=node.__class__.__name__,
                            invalid_state=sparkapi_pb2.InvalidState(
                                active=True,
                                error_msg=f'{ex.getErrorClass()} with {ex.getMessageParameters()} in node: {self.nodes[node_position].node_id}',  # noqa
                            ),
                            active=node.active,
                            columns=node.columns,
                            user_input=node.user_input_to_json() if include_user_input else '',
                        )
                    )
                break
        return recorded_spark_transforms
