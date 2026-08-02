from pyspark.sql.functions import current_date

POSTGRES_URL = "jdbc:postgresql://localhost:5432/retaildb"

POSTGRES_PROPERTIES = {
    "user": "postgres",
    "password": "postgres",   # Change if your password is different
    "driver": "org.postgresql.Driver",
}


def write_dataframe(df, table_name, mode="append"):
    (
        df.write
        .jdbc(
            url=POSTGRES_URL,
            table=table_name,
            mode=mode,
            properties=POSTGRES_PROPERTIES,
        )
    )