from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("To_Parquet").master("local[*]").getOrCreate()
df = (
    spark.read.option("delimiter", ";")
    .option("header", True)
    .csv("data/domains_small.csv")
)
df.coalesce(1).write.mode("overwrite").parquet("data/domains_small.parquet")
