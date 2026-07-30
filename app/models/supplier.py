from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True)

    supplier_name = Column(String(200), nullable=False)

    contact_name = Column(String(100))

    email = Column(String(255), unique=True)

    phone = Column(String(50))

    city = Column(String(100))

    state = Column(String(50))

    products = relationship(
        "Product",
        back_populates="supplier"
    )