from pyspark.sql import SparkSession
from pyspark.sql.functions import col, weekofyear, current_timestamp, current_date, date_format

if __name__ == "__main__":

    spark = SparkSession.builder \
        .appName("JobSity - Transformation") \
        .getOrCreate()

    df = spark.read.parquet("C:/datalake/jobsity/trips/raw")

    df = df.withColumn("trip_date", date_format(col("datetime"), "yyyy-MM-dd"))
    df = df.withColumn("trip_week", weekofyear(col("datetime")))
    df = df.drop("ingestion_date")

    df.write \
      .mode("overwrite") \
      .partitionBy("region", "trip_date") \
      .parquet("C:/datalake/jobsity/trips/transformed")

    spark.stop()