from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True)

    store_name = Column(
        String(200),
        nullable=False
    )

    city = Column(String(100))

    state = Column(String(50))

    inventory = relationship(
        "Inventory",
        back_populates="store"
    )