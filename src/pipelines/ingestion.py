from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, current_date, date_format

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("JobSity - Ingestion") \
        .config("spark.jars", "C:\\jars\\mysql-connector-j-8.1.0.jar") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    df = spark.read \
              .format("jdbc") \
              .option("url", "jdbc:mysql://127.0.0.1:3306/jobsity_db") \
              .option("driver", "com.mysql.cj.jdbc.Driver") \
              .option("dbtable", "trips") \
              .option("user", "jobsity_user") \
              .option("password", "password")  \
              .load()

    df = df.withColumn("ingestion_timestamp", current_timestamp())
    df = df.withColumn("ingestion_date", date_format(current_date(), "yyyy-MM-dd"))

    df.write \
      .mode("append") \
      .partitionBy("ingestion_date") \
      .parquet("C:/datalake/jobsity/trips/raw")

    spark.stop()