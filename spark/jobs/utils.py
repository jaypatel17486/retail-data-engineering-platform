from pyspark.sql import SparkSession

from spark.config.settings import APP_NAME


def create_spark():

    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .master("spark://spark-master:7077")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2",
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    return spark