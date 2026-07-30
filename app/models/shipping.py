from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database.database import Base


class Shipping(Base):
    __tablename__ = "shipping"

    shipping_id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id")
    )

    carrier = Column(String(100))

    tracking_number = Column(String(100))

    shipping_date = Column(DateTime)

    delivery_date = Column(DateTime)