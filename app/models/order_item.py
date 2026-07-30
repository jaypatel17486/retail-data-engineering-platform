from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
    )

    quantity = Column(Integer)
    unit_price = Column(Float)

    order = relationship("Order", back_populates="order_items")

    product = relationship("Product", back_populates="order_items")