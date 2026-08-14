import json
import os
import time
from datetime import datetime, timezone

import psycopg2
from kafka import KafkaConsumer, KafkaProducer

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

KAFKA_DLQ_TOPIC = os.getenv(
    "KAFKA_DLQ_TOPIC",
    "fluxguard-dead-letter",
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
    "fluxguard",
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
# RETRY CONFIGURATION
# =========================================================

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


# =========================================================
# POSTGRESQL CONNECTION
# =========================================================

def create_database_connection():
    """
    Create a PostgreSQL connection.
    """

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
# KAFKA CONSUMER
# =========================================================

def create_consumer():
    """
    Create the main FluxGuard Kafka consumer.

    Auto commit is disabled because FluxGuard commits
    offsets only after successful processing.
    """

    print("Connecting to Kafka consumer...")

    consumer = KafkaConsumer(
        KAFKA_TOPIC,

        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),

        group_id="fluxguard-fraud-engine",

        auto_offset_reset="latest",

        enable_auto_commit=False,
    )

    print("Connected to Kafka consumer.")

    return consumer


# =========================================================
# DEAD-LETTER PRODUCER
# =========================================================

def create_dlq_producer():
    """
    Create the Kafka producer used for the dead-letter queue.
    """

    print("Connecting to Kafka DLQ producer...")

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        value_serializer=lambda value: json.dumps(
            value
        ).encode("utf-8"),

        acks="all",

        retries=5,
    )

    print("Connected to Kafka DLQ producer.")

    return producer


# =========================================================
# SEND EVENT TO DLQ
# =========================================================

def send_to_dlq(
    producer,
    event,
    message,
    reason,
    error=None,
):
    """
    Preserve an event that cannot be processed.

    The original event and Kafka metadata are included so
    the failure can be investigated or replayed later.
    """

    dlq_event = {
        "original_event": event,

        "failure_reason": reason,

        "error_type": (
            type(error).__name__
            if error is not None
            else None
        ),

        "error_message": (
            str(error)
            if error is not None
            else None
        ),

        "source": {
            "topic": message.topic,
            "partition": message.partition,
            "offset": message.offset,
        },

        "failed_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    future = producer.send(
        KAFKA_DLQ_TOPIC,
        value=dlq_event,
    )

    # Wait until Kafka confirms that the DLQ message
    # was successfully written.
    metadata = future.get(
        timeout=10
    )

    print()
    print(
        f"[DLQ] Event sent successfully"
    )

    print(
        f"[DLQ] Topic     : "
        f"{metadata.topic}"
    )

    print(
        f"[DLQ] Partition : "
        f"{metadata.partition}"
    )

    print(
        f"[DLQ] Offset    : "
        f"{metadata.offset}"
    )


# =========================================================
# SAVE TRANSACTION
# =========================================================

def save_transaction(cursor, event):
    """
    Save the payment transaction.

    event_id is unique, making replayed Kafka events safe.
    """

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
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )

        ON CONFLICT (event_id)
        DO NOTHING
        """,
        (
            event["event_id"],
            event["order_id"],
            event["customer_id"],
            event["event_type"],
            event["amount"],
            event.get(
                "currency",
                "USD",
            ),
            event.get(
                "payment_method"
            ),
            event.get(
                "device_id"
            ),
            event.get(
                "ip_address"
            ),
            event.get(
                "billing_country"
            ),
            event.get(
                "shipping_country"
            ),
            event.get(
                "failure_reason"
            ),
            event["timestamp"],
        ),
    )


# =========================================================
# SAVE FRAUD PREDICTION
# =========================================================

def save_prediction(
    cursor,
    event,
    result,
):
    """
    Save rule, ML, and hybrid fraud predictions.
    """

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

        ON CONFLICT (event_id)
        DO NOTHING
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
# SAVE FRAUD ALERT
# =========================================================

def save_alert(
    cursor,
    event,
    result,
):
    """
    Create an alert only when the final decision is
    REVIEW or BLOCK.
    """

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
            %s, %s, %s,
            %s, %s, %s
        )

        ON CONFLICT (event_id)
        DO NOTHING
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

def process_payment(
    connection,
    event,
):
    """
    Analyze and persist one payment event.

    All database operations occur inside one transaction.
    """

    result = analyze_transaction(
        event
    )

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

        # Only commit when every database operation succeeds.
        connection.commit()

        return result

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()


# =========================================================
# PROCESS WITH RETRIES
# =========================================================

def process_with_retry(
    connection,
    event,
):
    """
    Retry processing when a temporary error occurs.
    """

    last_error = None

    for attempt in range(
        1,
        MAX_RETRIES + 1,
    ):
        try:
            return process_payment(
                connection,
                event,
            )

        except Exception as error:
            last_error = error

            print()
            print(
                f"[RETRY] Event: "
                f"{event.get('event_id')}"
            )

            print(
                f"[RETRY] Attempt: "
                f"{attempt}/{MAX_RETRIES}"
            )

            print(
                f"[RETRY] Error: "
                f"{type(error).__name__}: "
                f"{error}"
            )

            if attempt < MAX_RETRIES:
                print(
                    f"[RETRY] Waiting "
                    f"{RETRY_DELAY_SECONDS} "
                    f"seconds..."
                )

                time.sleep(
                    RETRY_DELAY_SECONDS
                )

    raise last_error


# =========================================================
# EVENT VALIDATION
# =========================================================

def get_missing_fields(event):
    """
    Return required fields missing from an event.
    """

    required_fields = (
        "event_id",
        "order_id",
        "customer_id",
        "event_type",
        "amount",
        "timestamp",
    )

    return [
        field
        for field in required_fields
        if event.get(field) is None
    ]


# =========================================================
# DISPLAY RESULT
# =========================================================

def print_result(
    event,
    result,
    message,
):
    """
    Display a successfully processed payment.
    """

    print()
    print("-" * 70)

    print(
        f"Event ID     : "
        f"{event['event_id']}"
    )

    print(
        f"Order        : "
        f"{event['order_id']}"
    )

    print(
        f"Customer     : "
        f"{event['customer_id']}"
    )

    print(
        f"Amount       : "
        f"${float(event['amount']):.2f}"
    )

    print(
        f"Payment      : "
        f"{event['event_type']}"
    )

    print(
        f"Rule Score   : "
        f"{result['rule_score']}"
    )

    print(
        f"Rule Risk    : "
        f"{result['rule_risk']}"
    )

    print(
        f"ML Prob.     : "
        f"{result['ml_probability']:.4f}"
    )

    print(
        f"ML Risk      : "
        f"{result['ml_risk']}"
    )

    print(
        f"Hybrid Score : "
        f"{result['hybrid_score']:.4f}"
    )

    print(
        f"Final Risk   : "
        f"{result['final_risk']}"
    )

    print(
        f"Decision     : "
        f"{result['final_decision']}"
    )

    print(
        f"Kafka        : "
        f"partition={message.partition}, "
        f"offset={message.offset}"
    )

    print(
        "Kafka Commit : SUCCESS"
    )

    print("-" * 70)


# =========================================================
# MAIN
# =========================================================

def run():
    """
    Run the FluxGuard real-time fraud consumer.
    """

    print()
    print("=" * 70)
    print(
        "FLUXGUARD REAL-TIME FRAUD ENGINE"
    )
    print("=" * 70)

    print(
        f"Kafka Server : "
        f"{KAFKA_BOOTSTRAP_SERVERS}"
    )

    print(
        f"Event Topic  : "
        f"{KAFKA_TOPIC}"
    )

    print(
        f"DLQ Topic    : "
        f"{KAFKA_DLQ_TOPIC}"
    )

    print(
        f"PostgreSQL   : "
        f"{POSTGRES_HOST}:"
        f"{POSTGRES_PORT}/"
        f"{POSTGRES_DB}"
    )

    print(
        "Consumer     : "
        "fluxguard-fraud-engine"
    )

    print(
        "Auto Commit  : DISABLED"
    )

    print(
        f"Max Retries  : "
        f"{MAX_RETRIES}"
    )

    print("=" * 70)

    connection = None
    consumer = None
    dlq_producer = None

    try:
        # =================================================
        # CONNECT
        # =================================================

        connection = (
            create_database_connection()
        )

        consumer = create_consumer()

        dlq_producer = (
            create_dlq_producer()
        )

        print()
        print(
            "Waiting for payment events..."
        )

        print(
            "Press Ctrl+C to stop."
        )

        # =================================================
        # EVENT LOOP
        # =================================================

        for message in consumer:

            event = message.value

            # ---------------------------------------------
            # IGNORE NON-PAYMENT EVENTS
            # ---------------------------------------------

            if event.get(
                "event_type"
            ) not in (
                "payment_completed",
                "payment_failed",
            ):
                # This event has been intentionally handled.
                consumer.commit()

                continue

            # ---------------------------------------------
            # VALIDATE
            # ---------------------------------------------

            missing_fields = (
                get_missing_fields(
                    event
                )
            )

            if missing_fields:
                print()
                print("=" * 70)
                print("INVALID EVENT")
                print("=" * 70)

                print(
                    f"Missing fields: "
                    f"{missing_fields}"
                )

                print(
                    f"Kafka partition: "
                    f"{message.partition}"
                )

                print(
                    f"Kafka offset: "
                    f"{message.offset}"
                )

                try:
                    # First preserve the event in the DLQ.
                    send_to_dlq(
                        dlq_producer,
                        event,
                        message,
                        reason=(
                            "missing_required_fields:"
                            + ",".join(
                                missing_fields
                            )
                        ),
                    )

                    # Only commit the original message after
                    # the DLQ write succeeds.
                    consumer.commit()

                    print(
                        "Original Kafka offset "
                        "committed."
                    )

                except Exception as dlq_error:
                    print()
                    print(
                        "[DLQ ERROR]"
                    )

                    print(
                        f"{type(dlq_error).__name__}: "
                        f"{dlq_error}"
                    )

                    print(
                        "Original Kafka offset "
                        "NOT committed."
                    )

                print("=" * 70)

                continue

            # ---------------------------------------------
            # PROCESS VALID PAYMENT
            # ---------------------------------------------

            try:
                result = (
                    process_with_retry(
                        connection,
                        event,
                    )
                )

                # IMPORTANT:
                #
                # PostgreSQL has already committed at this
                # point. Now we advance Kafka.

                consumer.commit()

                print_result(
                    event,
                    result,
                    message,
                )

            except Exception as error:
                # =========================================
                # ALL PROCESSING RETRIES FAILED
                # =========================================

                print()
                print("=" * 70)
                print(
                    "EVENT PROCESSING FAILED"
                )
                print("=" * 70)

                print(
                    f"Event ID: "
                    f"{event.get('event_id')}"
                )

                print(
                    f"Order ID: "
                    f"{event.get('order_id')}"
                )

                print(
                    f"Kafka partition: "
                    f"{message.partition}"
                )

                print(
                    f"Kafka offset: "
                    f"{message.offset}"
                )

                print(
                    f"Error: "
                    f"{type(error).__name__}: "
                    f"{error}"
                )

                # -----------------------------------------
                # DEAD LETTER
                # -----------------------------------------

                try:
                    send_to_dlq(
                        dlq_producer,
                        event,
                        message,
                        reason=(
                            "processing_failed_"
                            "after_retries"
                        ),
                        error=error,
                    )

                    # DLQ now safely owns the failed event.
                    # Advance the source topic offset.
                    consumer.commit()

                    print()
                    print(
                        "Original Kafka offset "
                        "committed after "
                        "successful DLQ write."
                    )

                except Exception as dlq_error:
                    # If DLQ itself fails, we intentionally
                    # leave the original offset uncommitted.

                    print()
                    print(
                        "DLQ WRITE FAILED"
                    )

                    print(
                        f"{type(dlq_error).__name__}: "
                        f"{dlq_error}"
                    )

                    print()
                    print(
                        "Original Kafka offset "
                        "NOT committed."
                    )

                    print(
                        "The source event may be "
                        "redelivered."
                    )

                print("=" * 70)

    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print(
            "Stopping FluxGuard fraud engine..."
        )
        print("=" * 70)

    except Exception as error:
        print()
        print("=" * 70)
        print(
            "FLUXGUARD CONSUMER ERROR"
        )
        print("=" * 70)

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        print("=" * 70)

        raise

    finally:
        # =================================================
        # CLEAN SHUTDOWN
        # =================================================

        if consumer is not None:
            print(
                "Closing Kafka consumer..."
            )

            consumer.close()

        if dlq_producer is not None:
            print(
                "Closing DLQ producer..."
            )

            try:
                dlq_producer.flush()
            finally:
                dlq_producer.close()

        if connection is not None:
            print(
                "Closing PostgreSQL connection..."
            )

            connection.close()

        print(
            "FluxGuard fraud engine stopped."
        )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run()