import json
import os

import psycopg2
from kafka import KafkaConsumer

from fraud.engine import analyze_transaction


# =========================================================
# CONFIGURATION
# =========================================================

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "fluxguard-events",
)

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "retaildb",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "postgres",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "postgres",
)


# =========================================================
# DATABASE
# =========================================================

def create_database_connection():
    print("Connecting to PostgreSQL...")

    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection.autocommit = False

    print("Connected to PostgreSQL.")

    return connection


# =========================================================
# STORE TRANSACTION
# =========================================================

def save_transaction(cursor, event):

    cursor.execute(
        """
        INSERT INTO transactions (
            event_id,
            order_id,
            customer_id,
            event_type,
            amount,
            currency,
            payment_method,
            device_id,
            ip_address,
            billing_country,
            shipping_country,
            failure_reason,
            event_timestamp
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (event_id) DO NOTHING
        """,
        (
            event["event_id"],
            event["order_id"],
            event["customer_id"],
            event["event_type"],
            event["amount"],
            event.get("currency", "USD"),
            event.get("payment_method"),
            event.get("device_id"),
            event.get("ip_address"),
            event.get("billing_country"),
            event.get("shipping_country"),
            event.get("failure_reason"),
            event["timestamp"],
        ),
    )


# =========================================================
# STORE FRAUD PREDICTION
# =========================================================

def save_prediction(cursor, event, result):

    cursor.execute(
        """
        INSERT INTO fraud_predictions (
            event_id,
            order_id,
            customer_id,
            rule_score,
            rule_risk,
            ml_probability,
            ml_risk,
            hybrid_score,
            final_risk,
            final_decision
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        """,
        (
            event["event_id"],
            event["order_id"],
            event["customer_id"],
            result["rule_score"],
            result["rule_risk"],
            result["ml_probability"],
            result["ml_risk"],
            result["hybrid_score"],
            result["final_risk"],
            result["final_decision"],
        ),
    )


# =========================================================
# STORE FRAUD ALERT
# =========================================================

def save_alert(cursor, event, result):

    # Only REVIEW/BLOCK transactions create an alert.
    if result["final_decision"] == "APPROVE":
        return

    cursor.execute(
        """
        INSERT INTO fraud_alerts (
            event_id,
            order_id,
            customer_id,
            risk_level,
            fraud_score,
            decision
        )
        VALUES (
            %s, %s, %s, %s, %s, %s
        )
        """,
        (
            event["event_id"],
            event["order_id"],
            event["customer_id"],
            result["final_risk"],
            result["hybrid_score"],
            result["final_decision"],
        ),
    )


# =========================================================
# PROCESS PAYMENT
# =========================================================

def process_payment(connection, event):

    result = analyze_transaction(event)

    cursor = connection.cursor()

    try:
        save_transaction(
            cursor,
            event,
        )

        save_prediction(
            cursor,
            event,
            result,
        )

        save_alert(
            cursor,
            event,
            result,
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()

    return result


# =========================================================
# KAFKA CONSUMER
# =========================================================

def create_consumer():

    print("Connecting to Kafka...")

    consumer = KafkaConsumer(
        KAFKA_TOPIC,

        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),

        group_id="fluxguard-fraud-engine",

        auto_offset_reset="latest",

        enable_auto_commit=True,
    )

    print("Connected to Kafka.")

    return consumer


# =========================================================
# MAIN
# =========================================================

def run():

    print()
    print("=" * 70)
    print("FLUXGUARD REAL-TIME FRAUD ENGINE")
    print("=" * 70)

    print(f"Kafka     : {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Topic     : {KAFKA_TOPIC}")
    print(
        f"Postgres  : "
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    print("=" * 70)

    connection = create_database_connection()

    consumer = create_consumer()

    print()
    print("Waiting for payment events...")
    print()

    try:

        for message in consumer:

            event = message.value

            # Ignore order_created events.
            if event.get("event_type") not in (
                "payment_completed",
                "payment_failed",
            ):
                continue

            try:

                result = process_payment(
                    connection,
                    event,
                )

                print("-" * 70)

                print(
                    f"Order       : "
                    f"{event['order_id']}"
                )

                print(
                    f"Customer    : "
                    f"{event['customer_id']}"
                )

                print(
                    f"Amount      : "
                    f"${event['amount']:.2f}"
                )

                print(
                    f"Payment     : "
                    f"{event['event_type']}"
                )

                print(
                    f"Rule Score  : "
                    f"{result['rule_score']}"
                )

                print(
                    f"ML Prob.    : "
                    f"{result['ml_probability']:.4f}"
                )

                print(
                    f"Hybrid Score: "
                    f"{result['hybrid_score']:.4f}"
                )

                print(
                    f"Risk        : "
                    f"{result['final_risk']}"
                )

                print(
                    f"Decision    : "
                    f"{result['final_decision']}"
                )

                print("-" * 70)

            except Exception as error:

                print(
                    f"Failed to process "
                    f"{event.get('event_id')}: {error}"
                )

    except KeyboardInterrupt:

        print()
        print("Stopping FluxGuard fraud engine...")

    finally:

        consumer.close()

        connection.close()

        print("FluxGuard fraud engine stopped.")


if __name__ == "__main__":
    run()