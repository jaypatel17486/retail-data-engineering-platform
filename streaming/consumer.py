import json

from kafka import KafkaConsumer

from app.repositories.streaming_repository import StreamingRepository


consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

repo = StreamingRepository()

print("=" * 60)
print("Listening for Kafka events...")
print("=" * 60)

try:

    for message in consumer:

        event = message.value

        repo.save(event)

        print(f"Saved Order {event['order_id']}")

except KeyboardInterrupt:

    print("\nStopping consumer...")

finally:

    repo.close()
    consumer.close()