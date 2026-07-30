import pandas as pd

from app.database.database import SessionLocal
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository


def load_customers():

    df = pd.read_csv("data/raw/customers.csv")

    db = SessionLocal()

    customers = []

    for _, row in df.iterrows():

        customers.append(
            Customer(
                customer_id=int(row["customer_id"]),
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                phone=row["phone"],
                city=row["city"],
                state=row["state"],
                created_at=row["created_at"],
            )
        )

        CustomerRepository.insert_many(db, customers)

    db.close()

    print(f"Inserted {len(customers)} customers")


if __name__ == "__main__":
    load_customers()