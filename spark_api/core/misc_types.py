from typing import TypedDict


class SparkActionMetadata(TypedDict):
    columns: str
    count: int
    schema: str
