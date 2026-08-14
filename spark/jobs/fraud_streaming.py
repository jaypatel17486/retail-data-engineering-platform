from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    to_timestamp,
    udf,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    BooleanType,
    ArrayType,
)

from spark.config.settings import (
    APP_NAME,
    KAFKA_BOOTSTRAP,
    KAFKA_TOPIC,
    CHECKPOINT_LOCATION,
)

from spark.schemas.order_schema import FLUXGUARD_EVENT_SCHEMA
from fraud.rules import calculate_fraud_score


# =========================================================
# SPARK SESSION
# =========================================================

spark = (
    SparkSession.builder
    .appName(f"{APP_NAME}-FraudDetection")
    .master("spark://spark-master:7077")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


print("=" * 70)
print("FLUXGUARD REAL-TIME FRAUD DETECTION")
print("=" * 70)
print(f"Kafka Server : {KAFKA_BOOTSTRAP}")
print(f"Kafka Topic  : {KAFKA_TOPIC}")
print("=" * 70)


# =========================================================
# FRAUD RESULT SCHEMA
# =========================================================

fraud_result_schema = StructType([
    StructField("fraud_score", IntegerType(), False),
    StructField("risk_level", StringType(), False),
    StructField("is_suspicious", BooleanType(), False),
    StructField(
        "fraud_reasons",
        ArrayType(StringType()),
        False
    ),
])


# =========================================================
# FRAUD UDF
# =========================================================

def score_payment(
    event_type,
    amount,
    billing_country,
    shipping_country,
    failure_reason,
):
    """
    Convert Spark columns into an event dictionary and
    pass it to the FluxGuard rule engine.
    """

    event = {
        "event_type": event_type,
        "amount": amount,
        "billing_country": billing_country,
        "shipping_country": shipping_country,
        "failure_reason": failure_reason,
    }

    return calculate_fraud_score(event)


fraud_udf = udf(
    score_payment,
    fraud_result_schema
)


# =========================================================
# READ KAFKA
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
# PARSE EVENTS
# =========================================================

events_df = (
    raw_df
    .select(
        from_json(
            col("value").cast("string"),
            FLUXGUARD_EVENT_SCHEMA
        ).alias("event")
    )
    .select("event.*")
)


# =========================================================
# VALIDATE EVENTS
# =========================================================

events_df = (
    events_df
    .filter(col("event_id").isNotNull())
    .filter(col("order_id").isNotNull())
    .filter(col("customer_id").isNotNull())
    .filter(col("event_type").isNotNull())
)


# =========================================================
# PAYMENT EVENTS ONLY
# =========================================================

payments_df = events_df.filter(
    col("event_type").isin(
        "payment_completed",
        "payment_failed",
    )
)


# =========================================================
# TIMESTAMP
# =========================================================

payments_df = payments_df.withColumn(
    "event_timestamp",
    to_timestamp(col("timestamp"))
)


# =========================================================
# DEDUPLICATION
# =========================================================

payments_df = (
    payments_df
    .withWatermark(
        "event_timestamp",
        "10 minutes"
    )
    .dropDuplicates(["event_id"])
)


# =========================================================
# FRAUD SCORING
# =========================================================

scored_df = payments_df.withColumn(
    "fraud_result",
    fraud_udf(
        col("event_type"),
        col("amount"),
        col("billing_country"),
        col("shipping_country"),
        col("failure_reason"),
    )
)


# =========================================================
# EXTRACT FRAUD RESULTS
# =========================================================

scored_df = (
    scored_df
    .withColumn(
        "fraud_score",
        col("fraud_result.fraud_score")
    )
    .withColumn(
        "risk_level",
        col("fraud_result.risk_level")
    )
    .withColumn(
        "is_suspicious",
        col("fraud_result.is_suspicious")
    )
    .withColumn(
        "fraud_reasons",
        col("fraud_result.fraud_reasons")
    )
    .drop("fraud_result")
)


# =========================================================
# OUTPUT
# =========================================================

output_df = scored_df.select(
    "event_id",
    "order_id",
    "customer_id",
    "event_type",
    "amount",
    "payment_method",
    "billing_country",
    "shipping_country",
    "failure_reason",
    "fraud_score",
    "risk_level",
    "is_suspicious",
    "fraud_reasons",
    "event_timestamp",
)


query = (
    output_df
    .writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", False)
    .option(
        "checkpointLocation",
        f"{CHECKPOINT_LOCATION}/fraud"
    )
    .start()
)


query.awaitTermination()