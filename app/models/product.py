from sqlalchemy import Column, Integer, String, Float

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(200))
    category = Column(String(100))
    price = Column(Float)
    stock_quantity = Column(Integer)