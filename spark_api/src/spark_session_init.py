from pyspark.sql import SparkSession


spark = (
    SparkSession.builder.appName("SparkSession")
    .master("local[*]")
    .config("spark.driver.memory", "30720m")
    .getOrCreate()
)
