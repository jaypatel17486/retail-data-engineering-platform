from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:

    @staticmethod
    def insert_many(db: Session, customers: list[Customer]):

        db.add_all(customers)

        db.commit()