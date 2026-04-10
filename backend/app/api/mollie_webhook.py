from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import logging
import requests

from app.db import SessionLocal
from app.repositories.payment_repository import PaymentRepository
from app.services.wallet_service import WalletService
from app.services.payment_finalizer import PaymentFinalizer
from app.services.redis_service import RedisPaymentService
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/webhooks/mollie",
    summary="Handle Mollie Webhook",
    description="""
Receives payment status updates from Mollie.

**Purpose:**
- Update payment status based on Mollie events
- Credit user's wallet when payment is successful
- Mark failed or canceled payments appropriately
- Ensure idempotency: repeated webhooks are ignored

**Request Body:**
- Mollie sends a `POST` with `id` of the payment

**Response:**
- `ok`: `true` if webhook was processed successfully
""",
    response_model=dict,
)
async def mollie_webhook(request: Request, db: Session = Depends(get_db)):
    # --- Read form data ---
    form = await request.form()
    mollie_id = form.get("id")

    logger.info("Mollie webhook called", {"id": mollie_id})

    if not mollie_id:
        return {"error": "invalid_webhook"}

    # Call Mollie API
    try:
        res = requests.get(
            f"https://api.mollie.com/v2/payments/{mollie_id}",
            headers={"Authorization": f"Bearer {settings.MOLLIE_API_KEY}"},
            timeout=10,
        )
        res.raise_for_status()
        mollie_payment = res.json()
    except Exception as e:
        logger.error("Mollie API error", {"error": str(e)})
        return {"ok": True}

    repo = PaymentRepository(db)
    wallet_service = WalletService(db)
    finalizer = PaymentFinalizer(db, repo)
    redis_service = RedisPaymentService()

    try:
        payment = repo.find_by_provider_payment_id("mollie", mollie_id)
    except Exception:
        logger.warning("Payment not found", {"provider_id": mollie_id})
        return {"ok": True}

    def logic():
        if payment.status in ["success", "failed"]:
            return

        mollie_amount = int(float(mollie_payment["amount"]["value"]) * 100)
        if mollie_amount != payment.amount:
            logger.error("Amount mismatch", {"payment_id": payment.id})
            return

        status = mollie_payment.get("status", "").lower()
        if status == "paid":
            try:
                wallet_service.credit_from_payment(payment)
                finalizer.succeed(payment)
            except Exception as e:
                finalizer.fail(payment, str(e))
        else:
            mapping = {
                "canceled": "psp_canceled_by_user",
                "expired": "psp_expired",
                "failed": "psp_failed",
            }
            reason = mapping.get(status, "psp_unknown")
            finalizer.fail(payment, reason)

    redis_service.with_lock(payment.id, logic)
    logger.info("Webhook processed successfully", {"payment_id": payment.id})
    return {"ok": True}
