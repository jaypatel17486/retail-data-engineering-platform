from sqlalchemy import Column, Integer, String, DateTime

from app.database.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True)
    phone = Column(String(50))
    city = Column(String(100))
    state = Column(String(10))
    created_at = Column(DateTime)