from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    to_timestamp,
)

from spark.config.settings import (
    APP_NAME,
    KAFKA_BOOTSTRAP,
    KAFKA_TOPIC,
    CHECKPOINT_LOCATION,
)

from spark.schemas.order_schema import FLUXGUARD_EVENT_SCHEMA


# =========================================================
# CREATE SPARK SESSION
# =========================================================

spark = (
    SparkSession.builder
    .appName(APP_NAME)
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


print("=" * 70)
print("FLUXGUARD SPARK STREAMING")
print("=" * 70)
print(f"Kafka Server : {KAFKA_BOOTSTRAP}")
print(f"Kafka Topic  : {KAFKA_TOPIC}")
print("=" * 70)


# =========================================================
# READ EVENTS FROM KAFKA
# =========================================================

raw_df = (
    spark.readStream
    .format("kafka")
    .option(
        "kafka.bootstrap.servers",
        KAFKA_BOOTSTRAP
    )
    .option(
        "subscribe",
        KAFKA_TOPIC
    )
    .option(
        "startingOffsets",
        "latest"
    )
    .load()
)


# =========================================================
# PARSE JSON
# =========================================================

parsed_df = (
    raw_df
    .selectExpr(
        "CAST(key AS STRING) AS kafka_key",
        "CAST(value AS STRING) AS json_value",
        "partition",
        "offset",
        "timestamp AS kafka_timestamp",
    )
    .select(
        "kafka_key",
        "partition",
        "offset",
        "kafka_timestamp",

        from_json(
            col("json_value"),
            FLUXGUARD_EVENT_SCHEMA
        ).alias("event")
    )
    .select(
        "kafka_key",
        "partition",
        "offset",
        "kafka_timestamp",
        "event.*",
    )
)


# =========================================================
# BASIC VALIDATION
# =========================================================

valid_df = (
    parsed_df
    .filter(col("event_id").isNotNull())
    .filter(col("event_type").isNotNull())
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
)


# =========================================================
# CONVERT EVENT TIMESTAMP
# =========================================================

valid_df = valid_df.withColumn(
    "event_timestamp",
    to_timestamp(col("timestamp"))
)


# =========================================================
# REMOVE DUPLICATE EVENTS
# =========================================================

deduplicated_df = (
    valid_df
    .withWatermark(
        "event_timestamp",
        "10 minutes"
    )
    .dropDuplicates(["event_id"])
)


# =========================================================
# SEPARATE EVENT TYPES
# =========================================================

orders_df = deduplicated_df.filter(
    col("event_type") == "order_created"
)


successful_payments_df = deduplicated_df.filter(
    col("event_type") == "payment_completed"
)


failed_payments_df = deduplicated_df.filter(
    col("event_type") == "payment_failed"
)


# =========================================================
# DISPLAY ALL VALID EVENTS
# =========================================================

query = (
    deduplicated_df
    .select(
        "event_id",
        "event_type",
        "order_id",
        "customer_id",
        "product_id",
        "total_amount",
        "amount",
        "payment_method",
        "failure_reason",
        "device_id",
        "billing_country",
        "shipping_country",
        "event_timestamp",
    )
    .writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .option(
        "checkpointLocation",
        f"{CHECKPOINT_LOCATION}/events"
    )
    .start()
)


query.awaitTermination()