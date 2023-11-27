from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, count, sum
from pyspark.sql.functions import broadcast
from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

def calculate_weekly_average(df, group_cols, report_name):
    df_agg = df.groupBy(group_cols + ["trip_week"]) \
        .agg(count("trip_week").alias("trip_count")) \
        .groupBy(*group_cols) \
        .agg(sum("trip_count").alias("trip_count_sum"),
             count("*").alias("region_count")) \
        .withColumn("weekly_average", col("trip_count_sum") / col("region_count")) \
        .select(
            lit(report_name).alias("report"),
            *group_cols,
            col("weekly_average")
        )
    return df_agg

def main():
    spark = SparkSession.builder \
        .appName("JobSity - Report Average Trips Weekly") \
        .getOrCreate()

    df = spark.read.parquet("C:/datalake/jobsity/datasets/trips_with_routes")

    df_region_week = calculate_weekly_average(df, ["region"], "region_weekly_average")
    df_region_route_week = calculate_weekly_average(df, ["region", "route"], "region_route_weekly_average")

    df_bouding_boxes = spark.read \
        .format("jdbc") \
        .option("url", "jdbc:mysql://127.0.0.1:3306/jobsity_db") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "bounding_boxes") \
        .option("user", "jobsity_user") \
        .option("password", "password")  \
        .load()

    df_bouding_boxes = df_bouding_boxes.withColumnRenamed("id", "bounding_box_id")
    df_bouding_boxes_broadcast = broadcast(df_bouding_boxes)

    df_with_bbox = df.join(df_bouding_boxes, 
                            (col("origin_x") >= col("x_min")) & 
                            (col("origin_x") <= col("x_max")) & 
                            (col("origin_y") >= col("y_min")) & 
                            (col("origin_y") <= col("y_max")))
    
    df_bbox_week = calculate_weekly_average(df_with_bbox, ["bounding_box_id"], "bounding_box_weekly_average")

    df_report = df_region_week \
        .unionByName(df_region_route_week, allowMissingColumns=True) \
        .unionByName(df_bbox_week, allowMissingColumns=True) \
        .withColumn("id", row_number().over(Window.orderBy("report", "region", "route", "bounding_box_id")))

    df_report.write \
        .format("jdbc") \
        .mode("overwrite") \
        .option("url", "jdbc:mysql://127.0.0.1:3306/jobsity_db") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "report_weekly_average") \
        .option("user", "jobsity_user") \
        .option("password", "password")  \
        .save() 

if __name__ == "__main__":
    main()
