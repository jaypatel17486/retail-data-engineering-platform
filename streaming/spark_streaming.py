from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    current_date,
)
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType,
)

from streaming.analytics import (
    build_product_summary,
    build_customer_summary,
    build_sales_summary,
)

from streaming.database_writer import write_dataframe


# ----------------------------------------
# Spark Session
# ----------------------------------------

spark = (
    SparkSession.builder
    .appName("Retail Streaming Pipeline")
    .config(
        "spark.jars.packages",
        ",".join([
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6",
            "org.postgresql:postgresql:42.7.3",
        ])
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ----------------------------------------
# Kafka Schema
# ----------------------------------------

order_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("product_id", IntegerType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("status", StringType(), True),
    StructField("timestamp", StringType(), True),
])

# ----------------------------------------
# Read Kafka Stream
# ----------------------------------------

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
        "latest"
    )
    .load()
)

# ----------------------------------------
# Convert JSON
# ----------------------------------------

orders_json = (
    orders.selectExpr(
        "CAST(value AS STRING)"
    )
)

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

# ----------------------------------------
# Validation
# ----------------------------------------

clean_orders = (
    parsed_orders
    .filter(col("quantity") > 0)
    .filter(col("price") > 0)
)

# ----------------------------------------
# Revenue
# ----------------------------------------

final_orders = (
    clean_orders
    .withColumn(
        "revenue",
        col("quantity") * col("price")
    )
)

# ----------------------------------------
# Process Each Micro Batch
# ----------------------------------------

def process_batch(batch_df, batch_id):

    if batch_df.isEmpty():
        print(f"Batch {batch_id}: Empty")
        return

    print(f"\n========== Batch {batch_id} ==========\n")

    batch_df.show(10, False)

    # ----------------------------------
    # Write Raw Orders
    # ----------------------------------

    write_dataframe(
        batch_df,
        "streaming_orders",
        mode="append",
    )

    # ----------------------------------
    # Product Analytics
    # ----------------------------------

    product_summary = build_product_summary(batch_df)

    product_summary.show()

    write_dataframe(
        product_summary,
        "product_summary",
        mode="overwrite",
    )

    # ----------------------------------
    # Customer Analytics
    # ----------------------------------

    customer_summary = build_customer_summary(batch_df)

    customer_summary.show()

    write_dataframe(
        customer_summary,
        "customer_summary",
        mode="overwrite",
    )

    # ----------------------------------
    # Sales Analytics
    # ----------------------------------

    sales_summary = (
        build_sales_summary(batch_df)
        .withColumn(
            "summary_date",
            current_date(),
        )
    )

    sales_summary.show()

    write_dataframe(
        sales_summary,
        "sales_summary",
        mode="overwrite",
    )

    print(f"Batch {batch_id} completed.")

# ----------------------------------------
# Streaming Query
# ----------------------------------------

query = (
    final_orders.writeStream
    .outputMode("append")
    .option(
        "checkpointLocation",
        "./checkpoints/orders"
    )
    .foreachBatch(process_batch)
    .start()
)

query.awaitTermination()