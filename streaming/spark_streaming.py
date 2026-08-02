from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = (
    SparkSession.builder
    .appName("RetailStreamingPipeline")
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6",
            "org.postgresql:postgresql:42.7.3"
        ])
    )
    .getOrCreate()
)

POSTGRES_URL = "jdbc:postgresql://localhost:5432/retaildb"

POSTGRES_PROPERTIES = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver",
}


# Kafka schema
order_schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("quantity", IntegerType()),
    StructField("price", DoubleType()),
    StructField("payment_method", StringType()),
    StructField("status", StringType()),
    StructField("timestamp", StringType())
])


# Read Kafka stream

orders = (
    spark.readStream
    .format("kafka")
    .option(
        "kafka.bootstrap.servers",
        "localhost:9092"
    )
    .option(
        "subscribe",
        "orders"
    )
    .option(
        "startingOffsets",
        "earliest"
    )
    .load()
)


# Convert Kafka value to string

orders_json = (
    orders
    .selectExpr(
        "CAST(value AS STRING)"
    )
)


# Parse JSON

parsed_orders = (
    orders_json
    .select(
        from_json(
            col("value"),
            order_schema
        ).alias("data")
    )
    .select("data.*")
)


# Data validation

clean_orders = (
    parsed_orders
    .filter(
        col("quantity") > 0
    )
    .filter(
        col("price") > 0
    )
)


# Calculate revenue

final_orders = (
    clean_orders
    .withColumn(
        "revenue",
        col("quantity") * col("price")
    )
)


# Output stream
def write_to_postgres(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    (
        batch_df.write
        .jdbc(
            url=POSTGRES_URL,
            table="streaming_orders",
            mode="append",
            properties=POSTGRES_PROPERTIES,
        )
    )

    print(f"Batch {batch_id} written to PostgreSQL")


query = (
    final_orders
    .writeStream
    .outputMode("append")
    .option(
        "checkpointLocation",
        "./checkpoints/streaming_orders"
    )
    .foreachBatch(write_to_postgres)
    .start()
)


query.awaitTermination()