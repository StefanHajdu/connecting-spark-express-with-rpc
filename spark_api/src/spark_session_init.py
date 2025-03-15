from pyspark.sql import SparkSession


spark = (
    SparkSession.builder.appName('SparkSession')
    .master('local[*]')
    .config('spark.driver.memory', '30720m')
    .config('spark.scheduler.mode', 'FAIR')
    .getOrCreate()
)
spark_app_id = spark._sc.applicationId

backslash_char = '\\'
print(rf"""
---------------------------    
                      _    
                     | |   
 ___ _ __   __ _ _ __| | __
/ __| '_ \ / _` | '__| |/ /
\__ \ |_) | (_| | |  |   < 
|___/ .__/ \__,_|_|  |_|\_{backslash_char}
    | |                    
    |_|""")

print(f'\nid: {spark_app_id}')
print('---------------------------\n')
