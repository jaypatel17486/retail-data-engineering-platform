import os

import psycopg2


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "retaildb"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
}


def load_dimensions(cursor):
    print("Loading dimensions...")

    # -----------------------------------------------------
    # CUSTOMERS
    # -----------------------------------------------------

    cursor.execute(
        """
        INSERT INTO fluxguard_dw.dim_customer (
            customer_id
        )
        SELECT DISTINCT
            customer_id
        FROM transactions
        WHERE customer_id IS NOT NULL

        ON CONFLICT (customer_id)
        DO NOTHING;
        """
    )

    # -----------------------------------------------------
    # PAYMENT METHODS
    # -----------------------------------------------------

    cursor.execute(
        """
        INSERT INTO fluxguard_dw.dim_payment_method (
            payment_method
        )
        SELECT DISTINCT
            payment_method
        FROM transactions
        WHERE payment_method IS NOT NULL

        ON CONFLICT (payment_method)
        DO NOTHING;
        """
    )

    # -----------------------------------------------------
    # DATE DIMENSION
    # -----------------------------------------------------

    cursor.execute(
        """
        INSERT INTO fluxguard_dw.dim_date (
            date_key,
            full_date,
            year,
            month,
            day,
            day_of_week
        )

        SELECT DISTINCT
            TO_CHAR(
                event_timestamp,
                'YYYYMMDD'
            )::INTEGER AS date_key,

            event_timestamp::DATE,

            EXTRACT(
                YEAR FROM event_timestamp
            )::INTEGER,

            EXTRACT(
                MONTH FROM event_timestamp
            )::INTEGER,

            EXTRACT(
                DAY FROM event_timestamp
            )::INTEGER,

            EXTRACT(
                DOW FROM event_timestamp
            )::INTEGER

        FROM transactions

        WHERE event_timestamp IS NOT NULL

        ON CONFLICT (date_key)
        DO NOTHING;
        """
    )

    print("Dimensions loaded.")


def load_transactions(cursor):
    print("Loading transaction facts...")

    cursor.execute(
        """
        INSERT INTO fluxguard_dw.fact_transactions (
            event_id,
            order_id,
            customer_key,
            payment_method_key,
            date_key,
            event_type,
            amount,
            currency,
            billing_country,
            shipping_country,
            event_timestamp
        )

        SELECT
            t.event_id,
            t.order_id,

            c.customer_key,

            p.payment_method_key,

            TO_CHAR(
                t.event_timestamp,
                'YYYYMMDD'
            )::INTEGER,

            t.event_type,
            t.amount,
            t.currency,
            t.billing_country,
            t.shipping_country,
            t.event_timestamp

        FROM transactions t

        LEFT JOIN fluxguard_dw.dim_customer c
            ON t.customer_id = c.customer_id

        LEFT JOIN fluxguard_dw.dim_payment_method p
            ON t.payment_method = p.payment_method

        ON CONFLICT (event_id)
        DO NOTHING;
        """
    )

    print("Transaction facts loaded.")


def load_fraud_predictions(cursor):
    print("Loading fraud predictions...")

    cursor.execute(
        """
        INSERT INTO fluxguard_dw.fact_fraud_predictions (
            event_id,
            order_id,
            rule_score,
            ml_probability,
            hybrid_score,
            final_risk,
            final_decision,
            created_at
        )

        SELECT
            event_id,
            order_id,
            rule_score,
            ml_probability,
            hybrid_score,
            final_risk,
            final_decision,
            created_at

        FROM fraud_predictions

        ON CONFLICT (event_id)
        DO NOTHING;
        """
    )

    print("Fraud predictions loaded.")


def load_fraud_alerts(cursor):
    print("Loading fraud alerts...")

    cursor.execute(
        """
        INSERT INTO fluxguard_dw.fact_fraud_alerts (
            event_id,
            order_id,
            risk_level,
            fraud_score,
            decision,
            status,
            created_at
        )

        SELECT
            event_id,
            order_id,
            risk_level,
            fraud_score,
            decision,
            status,
            created_at

        FROM fraud_alerts

        WHERE NOT EXISTS (
            SELECT 1
            FROM fluxguard_dw.fact_fraud_alerts existing
            WHERE existing.event_id = fraud_alerts.event_id
        );
        """
    )

    print("Fraud alerts loaded.")


def print_summary(cursor):
    print()
    print("=" * 60)
    print("FLUXGUARD WAREHOUSE SUMMARY")
    print("=" * 60)

    tables = [
        "dim_customer",
        "dim_payment_method",
        "dim_date",
        "fact_transactions",
        "fact_fraud_predictions",
        "fact_fraud_alerts",
    ]

    for table in tables:
        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM fluxguard_dw.{table};
            """
        )

        count = cursor.fetchone()[0]

        print(
            f"{table:<30} {count:>10}"
        )

    print("=" * 60)


def load_warehouse():
    print()
    print("=" * 60)
    print("FLUXGUARD WAREHOUSE LOAD")
    print("=" * 60)

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    cursor = connection.cursor()

    try:
        load_dimensions(cursor)

        load_transactions(cursor)

        load_fraud_predictions(cursor)

        load_fraud_alerts(cursor)

        connection.commit()

        print_summary(cursor)

        print()
        print(
            "FluxGuard warehouse load "
            "completed successfully."
        )

    except Exception as error:
        connection.rollback()

        print()
        print(
            "FluxGuard warehouse load failed."
        )

        print(
            f"{type(error).__name__}: {error}"
        )

        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    load_warehouse()