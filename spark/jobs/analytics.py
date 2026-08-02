from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    sum,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    FloatType,
    StringType,
)


spark = (
    SparkSession.builder
    .appName("RetailRevenueAnalytics")
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


# Read Kafka stream

raw_orders = (
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


# Convert JSON to columns

orders = (
    raw_orders
    .selectExpr(
        "CAST(value AS STRING) AS json"
    )
    .select(
        from_json(
            col("json"),
            schema
        ).alias("data")
    )
    .select("data.*")
)


# Revenue calculation

revenue = (
    orders
    .groupBy("payment_method")
    .agg(
        sum(
            col("price") * col("quantity")
        ).alias("total_revenue")
    )
)


# Output

query = (
    revenue.writeStream
    .format("console")
    .outputMode("complete")
    .option(
        "truncate",
        False
    )
    .start()
)


query.awaitTermination()