# app/models/wallet.py
from sqlalchemy import Column, Integer, BigInteger, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Wallet(Base, TimestampMixin):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    balance = Column(BigInteger, server_default="0", nullable=False)  # cents
    currency = Column(CHAR(3), server_default="EUR", nullable=False)

    # Relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship(
        "Transaction", back_populates="wallet", cascade="all, delete-orphan"
    )
