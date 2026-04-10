# app/models/payment.py
import uuid
from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    CHAR,
    Enum,
    ForeignKey,
    Text,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    gateway = Column(String(50), server_default="ideal", nullable=False)
    provider = Column(String(100), nullable=True)
    provider_payment_id = Column(String(100), nullable=True)
    provider_checkout_url = Column(Text, nullable=True)
    amount = Column(BigInteger, nullable=False)
    currency = Column(CHAR(3), server_default="EUR", nullable=False)
    status = Column(
        Enum("pending", "success", "failed", name="payment_status"), nullable=False, index=True
    )
    failure_reason = Column(String(255), nullable=True)
    idempotency_key = Column(String(255), nullable=False, unique=True)

    # Relationships
    user = relationship("User", back_populates="payments")
    transaction = relationship(
        "Transaction", back_populates="payment", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("provider", "provider_payment_id", name="provider_payment_unique"),
        Index("idx_user_status", "user_id", "status"),
    )
