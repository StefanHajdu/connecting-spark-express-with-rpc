from spark_session_init import spark


def spark_read_from_path(data_type: str, path: str):
    if data_type == 'csv':
        return spark.read.option('delimiter', ';').option('header', True).csv(path)
    elif data_type == 'json':
        return spark.read.json(path)
