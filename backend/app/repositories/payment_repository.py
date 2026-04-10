from sqlalchemy.orm import Session
from app.models.payment import Payment
import uuid
from app.repositories.contracts.payment_repository_interface import PaymentRepositoryInterface


class PaymentRepository(PaymentRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, id: str) -> Payment:
        payment = self.db.query(Payment).filter(Payment.id == id).first()
        if not payment:
            raise Exception("Payment not found")  # equal to findOrFail
        return payment

    def find_by_idempotency_key(self, key: str) -> Payment | None:
        return self.db.query(Payment).filter(Payment.idempotency_key == key).first()

    def find_by_provider_payment_id(self, provider: str, provider_payment_id: str) -> Payment:
        payment = (
            self.db.query(Payment)
            .filter(
                Payment.provider == provider, Payment.provider_payment_id == provider_payment_id
            )
            .first()
        )
        if not payment:
            raise Exception("Payment not found")
        return payment

    def create_pending(self, data: dict) -> Payment:
        payment = Payment(
            id=str(uuid.uuid4()),
            user_id=data["user_id"],
            gateway=data["gateway"],
            amount=data["amount"],
            currency="EUR",
            status="pending",
            idempotency_key=data["idempotency_key"],
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def mark_success(self, payment_id: str) -> bool:
        updated = (
            self.db.query(Payment)
            .filter(Payment.id == payment_id, Payment.status == "pending")
            .update({Payment.status: "success"})
        )

        self.db.commit()
        return updated == 1

    def mark_failed(self, payment_id: str, reason: str) -> bool:
        updated = (
            self.db.query(Payment)
            .filter(Payment.id == payment_id, Payment.status == "pending")
            .update(
                {
                    Payment.status: "failed",
                    Payment.failure_reason: reason,
                }
            )
        )

        self.db.commit()
        return updated == 1

    def mark_timed_out(self, payment: Payment) -> bool:
        updated = (
            self.db.query(Payment)
            .filter(Payment.id == payment.id, Payment.status == "pending")
            .update(
                {
                    Payment.status: "failed",
                    Payment.failure_reason: "processing_timeout",
                }
            )
        )

        if updated:
            self.db.commit()
            self.db.refresh(payment)
            return True

        return False

    def attach_provider_data(
        self,
        payment_id: str,
        provider: str,
        provider_payment_id: str,
        checkout_url: str,
    ) -> None:
        (
            self.db.query(Payment)
            .filter(Payment.id == payment_id)
            .update(
                {
                    Payment.provider: provider,
                    Payment.provider_payment_id: provider_payment_id,
                    Payment.provider_checkout_url: checkout_url,
                }
            )
        )
        self.db.commit()
