from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(200), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.supplier_id"),
        nullable=True,
    )
    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=True,
    )
    price = Column(Float)
    stock_quantity = Column(Integer)
    
    supplier = relationship(
        "Supplier",
        back_populates="products"
    )

    order_items = relationship(
        "OrderItem", 
        back_populates="product"
    )

    category = relationship(
        "Category",
        back_populates="products"
    )
    
    inventory = relationship(
        "Inventory",
        back_populates="product"
    )