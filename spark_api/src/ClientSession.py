import json

from constants import PLAN_NODE_ROOT_ID
from custom_types import SparkNode
from typing import Iterable


class ClientSession:
    def __init__(self, id):
        self.id = id

    def set_plan(self, plan):
        self.plan = plan

    def load_dataset(self, spark, path: str, file_type: str) -> SparkNode:
        self._log(f"/load: {path, file_type}")
        df = self._transform_load_by_path(spark, path, file_type)
        return {
            "df": df,
            "node_id": PLAN_NODE_ROOT_ID,
            "previous_node_id": None,
            "operation": f"{__name__}",
            "include_node": True,
            "query": "spark.read",
            "query_params_json": {"path": path, "file_type": file_type},
        }

    def _transform_load_by_path(self, spark, path: str, dataset_type: str):
        if dataset_type == "csv":
            return spark.read.option("delimiter", ";").option("header", True).csv(path)
        elif dataset_type == "json":
            return spark.read.json(path)

    def summarize(self, node_id: str):
        self._log(f"/summarize: {node_id}")
        return self.plan.summarize_node(node_id)

    def preview(self, node_id: str, limit: int) -> Iterable[str]:
        self._log(f"/preview {node_id}, {limit}")
        rows = self.plan.preview_node(node_id, limit)
        for row in rows:
            yield json.dumps(row)

    def _log(self, msg):
        print(f"    *** session - {self.id}] " + msg)
