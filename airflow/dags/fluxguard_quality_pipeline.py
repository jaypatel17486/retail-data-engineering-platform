from datetime import datetime

import psycopg2

from airflow import DAG
from airflow.operators.python import PythonOperator


DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "database": "fluxguard",
    "user": "postgres",
    "password": "postgres",
}


def run_quality_checks():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    try:
        # ---------------------------------------------
        # Check 1: Missing transaction IDs
        # ---------------------------------------------

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

        # ---------------------------------------------
        # Check 2: Invalid amounts
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE amount IS NULL
               OR amount < 0;
            """
        )

        invalid_amounts = cursor.fetchone()[0]

        # ---------------------------------------------
        # Check 3: Duplicate event IDs
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT event_id
                FROM transactions
                GROUP BY event_id
                HAVING COUNT(*) > 1
            ) duplicates;
            """
        )

        duplicate_events = cursor.fetchone()[0]

        # ---------------------------------------------
        # Check 4: Predictions without transactions
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM fraud_predictions fp

            LEFT JOIN transactions t
                ON fp.event_id = t.event_id

            WHERE t.event_id IS NULL;
            """
        )

        orphan_predictions = cursor.fetchone()[0]

        # ---------------------------------------------
        # Check 5: Invalid fraud scores
        # ---------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM fraud_predictions

            WHERE hybrid_score < 0
               OR hybrid_score > 1
               OR ml_probability < 0
               OR ml_probability > 1;
            """
        )

        invalid_scores = cursor.fetchone()[0]

        print("=" * 60)
        print("FLUXGUARD DATA QUALITY REPORT")
        print("=" * 60)

        print(f"Missing IDs:         {missing_ids}")
        print(f"Invalid amounts:     {invalid_amounts}")
        print(f"Duplicate events:    {duplicate_events}")
        print(f"Orphan predictions:  {orphan_predictions}")
        print(f"Invalid fraud scores:{invalid_scores}")

        total_errors = (
            missing_ids
            + invalid_amounts
            + duplicate_events
            + orphan_predictions
            + invalid_scores
        )

        if total_errors > 0:
            raise ValueError(
                f"FluxGuard quality checks failed: "
                f"{total_errors} issue(s)"
            )

        print()
        print("All FluxGuard quality checks passed.")

    finally:
        cursor.close()
        connection.close()


with DAG(
    dag_id="fluxguard_quality_pipeline",
    description="FluxGuard transaction and fraud data quality checks",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    tags=[
        "fluxguard",
        "quality",
    ],
) as dag:

    quality_check = PythonOperator(
        task_id="run_quality_checks",
        python_callable=run_quality_checks,
    )