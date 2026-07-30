from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    order_date = Column(DateTime)
    status = Column(String(50))

    customer = relationship("Customer", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order")

    payments = relationship("Payment", back_populates="order")

    shipping = relationship("Shipping", back_populates="order", uselist=False)