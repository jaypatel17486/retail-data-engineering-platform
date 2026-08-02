from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("SparkTest")
    .master("spark://spark-master:7077")
    .getOrCreate()
)


data = [
    ("Laptop", 1000),
    ("Phone", 500),
    ("Tablet", 300)
]


df = spark.createDataFrame(
    data,
    ["product", "price"]
)


df.show()


spark.stop()