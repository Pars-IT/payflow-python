# app/models/transaction.py
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    payment_id = Column(
        String(36), ForeignKey("payments.id"), nullable=True, unique=True, default=None
    )
    amount = Column(BigInteger, nullable=False)
    type = Column(Enum("credit", "debit", name="transaction_type"), nullable=False)

    # Relationships
    wallet = relationship("Wallet", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction", uselist=False)

    # Convenience methods
    def is_credit(self) -> bool:
        return self.type == "credit"

    def is_debit(self) -> bool:
        return self.type == "debit"
