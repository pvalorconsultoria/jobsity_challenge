import shutil

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, current_date, date_format, udf

from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

def name_cluster(cluster_id):
    return f"route-{cluster_id + 1}"

def save_model(model, model_path):
    # Verificar e excluir o diretório do modelo se ele já existir
    try:
        shutil.rmtree(model_path)
    except OSError:
        pass  # Se o diretório não existir, ignore

    model.save(model_path)

if __name__ == "__main__":

    spark = SparkSession.builder \
        .appName("JobSity - Grouping Trips") \
        .config("spark.jars", "C:\\jars\\mysql-connector-j-8.1.0.jar") \
        .getOrCreate()

    name_cluster_udf = udf(name_cluster)

    df = spark.read.parquet("C:/datalake/jobsity/trips/transformed")

    regions = df.select("region").distinct().rdd.flatMap(lambda x: x).collect()

    for region in regions:
        df_region = df.filter(col("region") == region)

        assembler = VectorAssembler(
            inputCols=["origin_x", "origin_y", "destination_x", "destination_y"], 
            outputCol="features"
        )

        kmeans = KMeans().setK(5).setSeed(42)

        pipeline = Pipeline(stages=[assembler, kmeans])

        model = pipeline.fit(df_region)

        model_path = f"C:/datalake/jobsity/models/routes_kmeans_{region}"

        save_model(model, model_path)

        predictions = model.transform(df_region)

        df_with_routes = predictions.withColumn("route", name_cluster_udf("prediction"))

        df_with_routes.select(
            "id", 
            "origin_x", 
            "origin_y", 
            "destination_x",
            "destination_y",
            "datetime",
            "datasource",
            "region",
            "trip_date",
            "trip_week",
            "route"
        ).write.mode("append") \
         .partitionBy("region", "route", "trip_week") \
         .parquet("C:/datalake/jobsity/datasets/trips_with_routes")
        
        df_with_routes.show()

