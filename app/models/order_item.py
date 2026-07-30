from sqlalchemy import Column, Integer, Float, ForeignKey

from app.database.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )

    quantity = Column(Integer)

    unit_price = Column(Float)