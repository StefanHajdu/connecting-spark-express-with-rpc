import grpc
import asyncio
import spark_call_pb2
import json
from pyspark.sql import SparkSession
import time

from typing import AsyncIterable
from spark_call_pb2_grpc import (
    SparkCallServicer,
    add_SparkCallServicer_to_server,
)

spark = (
    SparkSession.builder.appName("SparkSession")
    .master("local[1]")
    .config("spark.driver.memory", "2048m")
    .config("spark.driver.cores", "10")
    .getOrCreate()
)


def spark_read_dataframe(path: str, dataset_type: str):
    if dataset_type == "csv":
        return spark.read.option("delimiter", "\t").option("header", True).csv(path)
    elif dataset_type == "json":
        return spark.read.json(path)


df = spark_read_dataframe(
    "/home/stephenx/Documents/Programming/01_Blogs/rpc-with-spark-api/data/cars/cars.csv",
    "csv",
)


def stream_spark_df_rows(df):
    json_str_rows = df.limit(10).toPandas().to_json(orient="records")
    for row in json.loads(json_str_rows):
        row_json_obj = spark_call_pb2.DatasetRow(row_json=json.dumps(row))
        yield row_json_obj


class SparkCallServicer(SparkCallServicer):
    async def LoadDataset(
        self, request: spark_call_pb2.Dataset, unused_context
    ) -> AsyncIterable[spark_call_pb2.DatasetRow]:
        json_str_rows = df.limit(10).toPandas().to_json(orient="records")
        for row in json.loads(json_str_rows):
            time.sleep(1)
            row_json_obj = spark_call_pb2.DatasetRow(row_json=json.dumps(row))
            yield row_json_obj


async def serve():
    server = grpc.aio.server()
    add_SparkCallServicer_to_server(SparkCallServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(serve())
