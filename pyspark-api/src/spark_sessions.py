from pyspark.sql import SparkSession
from time import sleep


spark1 = (
    SparkSession.builder.appName("FirstSparkSession")
    .master("local[1]")
    .config("spark.driver.memory", "2048m")
    .config("spark.driver.cores", "10")
    .getOrCreate()
)

spark2 = (
    SparkSession.builder.appName("SecondSparkSession")
    .master("local[2]")
    .config("spark.driver.memory", "1024m")
    .config("spark.driver.cores", "5")
    .getOrCreate()
)

spark1.range(10).show()

spark2.range(5).show()

sleep(10000)
