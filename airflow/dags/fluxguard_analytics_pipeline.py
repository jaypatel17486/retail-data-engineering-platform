import os
from datetime import datetime

import psycopg2

from airflow import DAG
from airflow.operators.python import PythonOperator


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "retaildb"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}


# =========================================================
# DATABASE CHECK
# =========================================================

def check_database():
    connection = psycopg2.connect(**DB_CONFIG)

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT 1;")

        cursor.fetchone()

        print(
            "FluxGuard database connection successful."
        )

        cursor.close()

    finally:
        connection.close()


# =========================================================
# DATA QUALITY
# =========================================================

def run_quality_checks():
    connection = psycopg2.connect(**DB_CONFIG)

    cursor = connection.cursor()

    try:

        # Missing IDs
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE event_id IS NULL
               OR order_id IS NULL
               OR customer_id IS NULL;
            """
        )

        missing_ids = cursor.fetchone()[0]

        # Invalid amounts
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE amount IS NULL
               OR amount < 0;
            """
        )

        invalid_amounts = cursor.fetchone()[0]

        # Duplicate events
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT event_id
                FROM transactions
                GROUP BY event_id
                HAVING COUNT(*) > 1
            ) duplicate_events;
            """
        )

        duplicates = cursor.fetchone()[0]

        total_errors = (
            missing_ids
            + invalid_amounts
            + duplicates
        )

        print("FluxGuard Quality Check")
        print("-----------------------")
        print(f"Missing IDs:     {missing_ids}")
        print(f"Invalid amounts: {invalid_amounts}")
        print(f"Duplicates:      {duplicates}")

        if total_errors > 0:
            raise ValueError(
                f"Data quality failed with "
                f"{total_errors} issue(s)."
            )

        print("Data quality checks passed.")

    finally:
        cursor.close()
        connection.close()


# =========================================================
# WAREHOUSE LOAD
# =========================================================

def load_fluxguard_warehouse():
    """
    Import here so Airflow loads the warehouse code
    only when this task executes.
    """

    from warehouse.loaders.load_fluxguard_warehouse import (
        load_warehouse,
    )

    load_warehouse()


# =========================================================
# ANALYTICS SUMMARY
# =========================================================

def calculate_warehouse_metrics():
    connection = psycopg2.connect(**DB_CONFIG)

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT
                COUNT(*) AS transactions,

                COALESCE(
                    SUM(amount) FILTER (
                        WHERE event_type = 'payment_completed'
                    ),
                    0
                ) AS revenue,

                COALESCE(
                    AVG(amount),
                    0
                ) AS average_transaction_value

            FROM fluxguard_dw.fact_transactions;
            """
        )

        transaction_result = cursor.fetchone()

        cursor.execute(
            """
            SELECT
                COUNT(*) AS predictions,

                COUNT(*) FILTER (
                    WHERE final_risk = 'HIGH'
                ) AS high_risk,

                COUNT(*) FILTER (
                    WHERE final_decision = 'BLOCK'
                ) AS blocked

            FROM fluxguard_dw.fact_fraud_predictions;
            """
        )

        fraud_result = cursor.fetchone()

        print()
        print("=" * 60)
        print("FLUXGUARD WAREHOUSE ANALYTICS")
        print("=" * 60)

        print(
            f"Transactions: "
            f"{transaction_result[0]}"
        )

        print(
            f"Revenue: "
            f"${transaction_result[1]}"
        )

        print(
            f"Average Transaction: "
            f"${transaction_result[2]}"
        )

        print(
            f"Fraud Predictions: "
            f"{fraud_result[0]}"
        )

        print(
            f"High Risk: "
            f"{fraud_result[1]}"
        )

        print(
            f"Blocked: "
            f"{fraud_result[2]}"
        )

        print("=" * 60)

    finally:
        cursor.close()
        connection.close()


# =========================================================
# DAG
# =========================================================

with DAG(
    dag_id="fluxguard_analytics_pipeline",

    description=(
        "FluxGuard automated quality, warehouse, "
        "and historical analytics pipeline"
    ),

    start_date=datetime(2026, 8, 1),

    schedule="@daily",

    catchup=False,

    tags=[
        "fluxguard",
        "warehouse",
        "analytics",
    ],

) as dag:

    database_check = PythonOperator(
        task_id="check_database",
        python_callable=check_database,
    )

    quality_check = PythonOperator(
        task_id="quality_check",
        python_callable=run_quality_checks,
    )

    warehouse_load = PythonOperator(
        task_id="load_warehouse",
        python_callable=load_fluxguard_warehouse,
    )

    analytics_summary = PythonOperator(
        task_id="warehouse_analytics",
        python_callable=calculate_warehouse_metrics,
    )


    (
        database_check
        >> quality_check
        >> warehouse_load
        >> analytics_summary
    )