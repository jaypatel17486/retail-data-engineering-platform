from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    FloatType,
    StringType,
)


spark = (
    SparkSession.builder
    .appName("RetailStreaming")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", FloatType(), True),
    StructField("payment_method", StringType(), True),
    StructField("status", StringType(), True),
    StructField("timestamp", StringType(), True),
])


raw_df = (
    spark.readStream
    .format("kafka")
    .option(
        "kafka.bootstrap.servers",
        "kafka:9092"
    )
    .option(
        "subscribe",
        "orders"
    )
    .option(
        "startingOffsets",
        "latest"
    )
    .load()
)


orders_df = (
    raw_df
    .selectExpr(
        "CAST(value AS STRING) AS json"
    )
    .select(
        from_json(
            col("json"),
            schema
        ).alias("order")
    )
    .select(
        "order.*"
    )
)


query = (
    orders_df.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .start()
)


query.awaitTermination()