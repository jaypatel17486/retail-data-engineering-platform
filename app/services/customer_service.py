import pandas as pd

from app.database.database import SessionLocal
from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerService:

    def load_customers(self):

        db = SessionLocal()

        repo = BaseRepository(db)

        df = pd.read_csv("data/raw/customers.csv")

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

        repo.add_many(customers)

        db.close()

        print(f"Inserted {len(customers)} customers")