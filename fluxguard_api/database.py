import os

from psycopg2.pool import SimpleConnectionPool


DB_POOL = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
    database=os.getenv("POSTGRES_DB", "retaildb"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
)


def get_connection():
    return DB_POOL.getconn()


def release_connection(connection):
    DB_POOL.putconn(connection)


def close_pool():
    DB_POOL.closeall()