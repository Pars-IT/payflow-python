from app.services.redis_service import RedisPaymentService
from app.events.event_bus import EventBus
from app.events.payment_events import PaymentSucceeded, PaymentFailed


class PaymentFinalizer:
    def __init__(self, db, repo):
        self.db = db
        self.repo = repo
        self.redis = RedisPaymentService()

    def succeed(self, payment):
        try:
            updated = self.repo.mark_success(payment.id)
            if not updated:
                print(f"[DEBUG] Payment {payment.id} already finalized")
                return

            self.redis.set_payment_state(payment.id, {"status": "success"})
            EventBus.dispatch(PaymentSucceeded(payment))

            print(f"[DEBUG] Payment {payment.id} marked success")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Failed to finalize payment {payment.id}: {e}")
            raise

    def fail(self, payment, reason):
        try:
            updated = self.repo.mark_failed(payment.id, reason)
            if not updated:
                print(f"[DEBUG] Payment {payment.id} already finalized")
                return

            self.redis.set_payment_state(payment.id, {"status": "failed", "failure_reason": reason})
            EventBus.dispatch(PaymentFailed(payment, reason))

            print(f"[DEBUG] Payment {payment.id} marked failed: {reason}")
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] Failed to fail payment {payment.id}: {e}")
            raise
