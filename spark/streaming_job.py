from spark.session import spark

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "orders")
    .load()
)

query = (
    df.selectExpr("CAST(value AS STRING)")
      .writeStream
      .format("console")
      .outputMode("append")
      .start()
)

query.awaitTermination()