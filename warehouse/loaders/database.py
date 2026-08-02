import psycopg2
from psycopg2.extras import DictCursor

from config.database import DB_CONFIG


def get_connection():
    return psycopg2.connect(
        cursor_factory=DictCursor,
        **DB_CONFIG,
    )