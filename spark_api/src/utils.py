import sparkapi_pb2
from exceptions import InvalidSparkInputException

from spark_session_init import spark


def load_data_for_spark(input_metadata: sparkapi_pb2.CsvInput | sparkapi_pb2.JsonInput | sparkapi_pb2.ParquetInput):
    if isinstance(input_metadata, sparkapi_pb2.CsvInput):
        return (
            spark.read.option('delimiter', input_metadata.delimiter)
            .option('header', input_metadata.include_header)
            .option('inferSchema', True)
            .csv(input_metadata.path)
        )
    elif isinstance(input_metadata, sparkapi_pb2.JsonInput):
        return spark.read.option('multiline', input_metadata.multiline).json(input_metadata.path)
    elif isinstance(input_metadata, sparkapi_pb2.ParquetInput):
        return spark.read.parquet(input_metadata.path)
    else:
        raise InvalidSparkInputException()
