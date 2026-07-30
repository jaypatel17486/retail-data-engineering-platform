from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True)

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
    )

    store_id = Column(
        Integer,
        ForeignKey("stores.store_id"),
        nullable=False,
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0,
    )

    product = relationship(
        "Product",
        back_populates="inventory",
    )

    store = relationship(
        "Store",
        back_populates="inventory",
    )