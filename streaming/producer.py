import json
import time

from kafka import KafkaProducer

from streaming.events import generate_order_event


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print("=" * 60)
print("🚀 Connected to Kafka")
print("Sending retail order events...")
print("=" * 60)

try:
    while True:

        event = generate_order_event()

        producer.send(
            "orders",
            event,
        )

        producer.flush()

        print(event)

        time.sleep(2)

except KeyboardInterrupt:

    print("\nStopping producer...")

finally:

    producer.close()

    print("Producer closed.")