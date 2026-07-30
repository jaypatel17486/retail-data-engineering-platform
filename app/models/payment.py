from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey

from app.database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id")
    )

    payment_method = Column(String(50))

    amount = Column(Float)

    payment_date = Column(DateTime)