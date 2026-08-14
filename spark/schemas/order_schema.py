from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)


FLUXGUARD_EVENT_SCHEMA = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_type", StringType(), False),

    StructField("order_id", StringType(), False),
    StructField("customer_id", StringType(), False),

    # Order fields
    StructField("product_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("total_amount", DoubleType(), True),

    # Payment fields
    StructField("amount", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("ip_address", StringType(), True),
    StructField("billing_country", StringType(), True),
    StructField("shipping_country", StringType(), True),
    StructField("failure_reason", StringType(), True),

    StructField("currency", StringType(), True),
    StructField("timestamp", StringType(), False),
    StructField("transaction_profile", StringType(), True),
    StructField("is_fraud", IntegerType(), True)
])