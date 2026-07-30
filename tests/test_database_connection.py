from app.database.database import SessionLocal


def test_connection():

    db = SessionLocal()

    print("Database connection successful!")

    db.close()


if __name__ == "__main__":
    test_connection()