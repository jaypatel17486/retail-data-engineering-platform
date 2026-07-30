from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    payment_method = Column(String(50))
    amount = Column(Float)
    payment_date = Column(DateTime)

    order = relationship("Order", back_populates="payments")