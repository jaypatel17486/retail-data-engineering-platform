from pyspark.sql.functions import *


def build_product_summary(df):
    return (
        df.groupBy("product_id")
        .agg(
            sum("quantity").alias("total_quantity"),
            sum("revenue").alias("total_revenue"),
        )
    )


def build_customer_summary(df):
    return (
        df.groupBy("customer_id")
        .agg(
            count("order_id").alias("total_orders"),
            sum("revenue").alias("total_spent"),
        )
    )


def build_sales_summary(df):
    return (
        df.agg(
            count("order_id").alias("total_orders"),
            sum("revenue").alias("total_revenue"),
            avg("revenue").alias("average_order_value"),
        )
    )