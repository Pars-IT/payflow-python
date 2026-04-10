# app/jobs/payment_job.py

from app.celery_app import celery
from app.db import SessionLocal
from app.repositories.payment_repository import PaymentRepository
from app.services.redis_service import RedisPaymentService
from app.services.payment_finalizer import PaymentFinalizer
from app.payments.resolver import GatewayResolver
from app.services.wallet_service import WalletService


@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def process_payment(self, payment_id):
    db = SessionLocal()

    try:
        repo = PaymentRepository(db)
        redis_service = RedisPaymentService()
        finalizer = PaymentFinalizer(db, repo)
        wallet_service = WalletService(db)
        resolver = GatewayResolver()

        def logic():
            payment = repo.find_by_id(payment_id)

            if not payment or payment.status != "pending":
                return

            try:
                gateway = resolver.resolve(payment)
                result = gateway.charge(payment)

                if not result.success:
                    finalizer.fail(payment, result.reason)
                    return

                if result.async_flow:
                    repo.attach_provider_data(
                        payment.id, payment.gateway, result.provider_payment_id, result.checkout_url
                    )
                    return

                wallet_service.credit_from_payment(payment)
                finalizer.succeed(payment)

            except Exception as e:
                finalizer.fail(payment, str(e))
                raise e  # important for retry

        redis_service.with_lock(payment_id, logic)

    except Exception:
        if self.request.retries >= 3:
            print(f"DLQ: payment {payment_id} failed permanently")

        raise

    finally:
        db.close()
