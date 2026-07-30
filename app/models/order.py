from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id")
    )

    order_date = Column(DateTime)

    status = Column(String(50))