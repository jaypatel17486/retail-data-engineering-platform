from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True)

    category_name = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    products = relationship(
        "Product",
        back_populates="category"
    )