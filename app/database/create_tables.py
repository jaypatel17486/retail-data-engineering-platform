from app.database.database import Base, engine

# Import all models here
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.shipping import Shipping


def create_tables():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("All tables created successfully!")


if __name__ == "__main__":
    create_tables()