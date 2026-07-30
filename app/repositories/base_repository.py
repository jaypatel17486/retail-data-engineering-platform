from sqlalchemy import text
from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def truncate(self, table_name: str):

        self.db.execute(
            text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
        )

        self.db.commit()

    def add_many(self, objects):

        try:
            self.db.add_all(objects)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise