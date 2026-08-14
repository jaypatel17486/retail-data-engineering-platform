import json
import os
import time

from kafka import KafkaProducer


from streaming.events import generate_transaction


# =========================================================
# FLUXGUARD KAFKA CONFIGURATION
# =========================================================

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "fluxguard-events"
)


# =========================================================
# CREATE KAFKA PRODUCER
# =========================================================

def create_producer():
    """
    Create and return the Kafka producer.
    """

    print("Connecting to Kafka...")
    print(f"Kafka server: {KAFKA_BOOTSTRAP_SERVERS}")

    try:
        kafka_producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

            # Convert Python dictionary -> JSON -> bytes
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),

            # Use order_id as Kafka message key
            key_serializer=lambda key: key.encode("utf-8"),

            # Wait for Kafka acknowledgement
            acks="all",

            # Retry temporary failures
            retries=5,
        )

        print("Connected to Kafka successfully.")
        return kafka_producer

    except Exception as error:
        print()
        print("ERROR: Could not connect to Kafka.")
        print(f"Kafka server: {KAFKA_BOOTSTRAP_SERVERS}")
        print(f"Error details: {error}")
        
        raise
    


# =========================================================
# SEND EVENT
# =========================================================

def send_event(producer, event):
    """
    Send one FluxGuard event to Kafka.

    Using order_id as the Kafka key helps keep events for the
    same order in the same Kafka partition.
    """

    order_id = event["order_id"]

    future = producer.send(
        KAFKA_TOPIC,
        key=order_id,
        value=event,
    )

    # Wait for Kafka acknowledgement.
    # This is useful while developing/debugging.
    metadata = future.get(timeout=10)

    return metadata


# =========================================================
# PRINT EVENT
# =========================================================

def print_order_event(event):
    print(
        f"[ORDER]   "
        f"{event['event_type']} | "
        f"{event['order_id']} | "
        f"customer={event['customer_id']} | "
        f"amount=${event['total_amount']:.2f}"
    )


def print_payment_event(event):
    print(
        f"[PAYMENT] "
        f"{event['event_type']} | "
        f"{event['order_id']} | "
        f"customer={event['customer_id']} | "
        f"amount=${event['amount']:.2f}"
    )


# =========================================================
# MAIN PRODUCER LOOP
# =========================================================

def run_producer():
    print()
    print("=" * 70)
    print("FLUXGUARD")
    print("Real-Time E-Commerce Analytics & Fraud Detection Platform")
    print("=" * 70)

    print(f"Kafka Topic : {KAFKA_TOPIC}")
    print(f"Kafka Server: {KAFKA_BOOTSTRAP_SERVERS}")

    print("=" * 70)

    producer = None

    try:
        # -------------------------------------------------
        # Connect to Kafka
        # -------------------------------------------------

        producer = create_producer()

        print()
        print("FluxGuard transaction producer started.")
        print("Press Ctrl+C to stop.")
        print()

        transaction_count = 0

        # -------------------------------------------------
        # Produce transactions continuously
        # -------------------------------------------------

        while True:
            transaction_count += 1

            # Generate correlated order + payment events
            order_event, payment_event = generate_transaction()

            print("-" * 70)
            print(f"Transaction #{transaction_count}")

            # -------------------------------------------------
            # ORDER CREATED
            # -------------------------------------------------

            order_metadata = send_event(
                producer,
                order_event
            )

            print_order_event(order_event)

            print(
                f"          Kafka partition={order_metadata.partition} "
                f"offset={order_metadata.offset}"
            )

            # -------------------------------------------------
            # PAYMENT EVENT
            # -------------------------------------------------

            payment_metadata = send_event(
                producer,
                payment_event
            )

            print_payment_event(payment_event)

            print(
                f"          Kafka partition={payment_metadata.partition} "
                f"offset={payment_metadata.offset}"
            )

            # -------------------------------------------------
            # Verify correlation
            # -------------------------------------------------

            if (
                order_event["order_id"] == payment_event["order_id"]
                and
                order_event["customer_id"] == payment_event["customer_id"]
                and
                order_event["total_amount"] == payment_event["amount"]
            ):
                print("          Transaction correlation: OK")

            else:
                print("          WARNING: Transaction correlation failed!")

            print("-" * 70)

            # Generate a new transaction every 2 seconds
            time.sleep(2)

    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("Stopping FluxGuard producer...")
        print("=" * 70)

    except Exception as error:
        print()
        print("=" * 70)
        print("FLUXGUARD PRODUCER ERROR")
        print("=" * 70)
        print(f"{type(error).__name__}: {error}")
        print("=" * 70)

        raise

    finally:
        if producer is not None:
            print("Flushing Kafka messages...")
            producer.flush()

            print("Closing Kafka producer...")
            producer.close()

        print("FluxGuard producer stopped.")


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    run_producer()