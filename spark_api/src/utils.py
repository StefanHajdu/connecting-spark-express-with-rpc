import os

from custom_exceptions import InvalidSparkInputException
from spark_session_init import spark


def spark_read_from_path(path: str):
    _, file_extension = os.path.splitext(path)
    if file_extension == '.csv':
        return spark.read.option('delimiter', ';').option('header', True).option('inferSchema', True).csv(path)
    elif file_extension == '.json':
        return spark.read.option('multiline', 'true').json(path)
    elif file_extension == '.parquet':
        return spark.read.parquet(path)
    else:
        raise InvalidSparkInputException()


def get_dir_size(path: str):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total
