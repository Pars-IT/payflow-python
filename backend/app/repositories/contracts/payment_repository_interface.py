from abc import ABC, abstractmethod
from app.models.payment import Payment


class PaymentRepositoryInterface(ABC):
    @abstractmethod
    def find_by_id(self, id: str) -> Payment:
        pass

    @abstractmethod
    def find_by_idempotency_key(self, key: str) -> Payment | None:
        pass

    @abstractmethod
    def find_by_provider_payment_id(self, provider: str, provider_payment_id: str) -> Payment:
        pass

    @abstractmethod
    def create_pending(self, data: dict) -> Payment:
        pass

    @abstractmethod
    def mark_success(self, payment_id: str) -> bool:
        pass

    @abstractmethod
    def mark_failed(self, payment_id: str, reason: str) -> bool:
        pass
