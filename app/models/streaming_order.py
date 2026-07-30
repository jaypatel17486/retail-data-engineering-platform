from sqlalchemy import Column, Integer, Float, String

from app.database.database import Base


class StreamingOrder(Base):

    __tablename__ = "streaming_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    payment_method = Column(String(50))
    status = Column(String(50))
    timestamp = Column(String(100))