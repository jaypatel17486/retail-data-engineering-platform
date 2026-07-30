from app.database.database import Base, engine

from app.models import (
    Customer,
    Product,
    Order,
    OrderItem,
    Payment,
    Shipping,
    Supplier,
    Category,
    Store,
    Inventory,
)


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")


if __name__ == "__main__":
    create_tables()