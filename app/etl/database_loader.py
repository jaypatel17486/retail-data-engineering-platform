from app.database.database import SessionLocal
from app.repositories.base_repository import BaseRepository


class DatabaseLoader:

    def __init__(self):

        self.db = SessionLocal()

        self.repo = BaseRepository(self.db)

    def load(self, table_name, objects):

        self.repo.truncate(table_name)

        self.repo.add_many(objects)

    def close(self):

        self.db.close()