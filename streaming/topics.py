from kafka.admin import KafkaAdminClient, NewTopic


admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id="retail-admin",
)

topic = NewTopic(
    name="orders",
    num_partitions=3,
    replication_factor=1,
)

try:
    admin.create_topics([topic])
    print("Topic created.")
except Exception as e:
    print(e)

admin.close()