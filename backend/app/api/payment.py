# app/api/payment.py

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.db import SessionLocal
from app.repositories.payment_repository import PaymentRepository
from app.jobs.payment_job import process_payment
from app.services.redis_service import RedisPaymentService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/payments",
    summary="Create a Payment",
    description="""
Initiates a new payment for a user with the specified gateway.

**Purpose:**
- Create a pending payment in the system
- Return information needed for frontend checkout (e.g., payment ID)
- Prevent duplicate payments using `idempotency_key`

**Request Body:**
- `user_id`: ID of the user making the payment
- `amount`: Payment amount in cents
- `gateway`: Payment gateway key
- `idempotency_key`: Unique key to ensure request idempotency

**Response:**
- Payment object with status `pending` and generated `id`
""",
    response_model=dict,
)
def create_payment(
    user_id: int = Form(...),
    amount: int = Form(..., gt=0),
    idempotency_key: str = Form(...),
    gateway: str = Form(...),
    db: Session = Depends(get_db),
):
    repo = PaymentRepository(db)

    existing = repo.find_by_idempotency_key(idempotency_key)
    if existing:
        return get_payment(existing.id, db)

    payment = repo.create_pending(
        {
            "user_id": user_id,
            "gateway": gateway,
            "amount": amount,
            "idempotency_key": idempotency_key,
        }
    )

    process_payment.delay(payment.id)
    return {"id": payment.id, "status": payment.status}


@router.get(
    "/payments/{payment_id}",
    summary="Get Payment Status",
    description="""
Fetches the current status and details of a specific payment.

**Purpose:**
- Check if a payment is pending, successful, or failed
- Return cached payment state if available
- Auto-heal payments stuck in `pending` status
- Useful for frontend checkout status updates

**Path Parameters:**
- `payment_id`: The unique ID of the payment to fetch

**Response:**
- `id`: Payment ID
- `status`: Current status (`pending`, `success`, `failed`)
- `amount`: Payment amount in cents
- `failure_reason`: Reason for failure if any
- `checkout_url`: URL for completing payment if pending
- `cached`: `true` if the response came from cache
""",
    response_model=dict,
)
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    repo = PaymentRepository(db)
    redis_service = RedisPaymentService()

    # 1. cache
    state = redis_service.get_payment_state(payment_id)
    if state:
        return {"id": payment_id, "cached": True, **state}

    # 2. db fallback
    try:
        payment = repo.find_by_id(payment_id)
    except Exception:
        return {"error": "not_found"}

    if not payment:
        return {"error": "not_found"}

    # 3. auto-heal timeout
    if (
        payment.status == "pending"
        and payment.provider_checkout_url is None
        and payment.created_at < datetime.now(timezone.utc) - timedelta(minutes=1)
    ):
        repo.mark_failed(payment.id, "processing_timeout")

    response = {
        "id": payment.id,
        "status": payment.status,
        "amount": payment.amount,
        "failure_reason": payment.failure_reason,
        "checkout_url": payment.provider_checkout_url,
    }

    # 4. cache warm
    if payment.status in ["success", "failed"] or payment.provider_checkout_url:
        redis_service.set_payment_state(payment.id, response)

    return response
