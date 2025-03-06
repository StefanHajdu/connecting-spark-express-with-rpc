from pyspark.sql import DataFrame
from typing import TypedDict


class SparkNode(TypedDict):
    df: DataFrame
    node_id: str
    previous_node_id: str
    operation: str
    include_node: bool
    query: str
    query_params_json: str
