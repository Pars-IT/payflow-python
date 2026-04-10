# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    wallet = relationship(
        "Wallet", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
