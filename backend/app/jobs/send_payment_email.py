# app/jobs/send_payment_email.py
from app.db import SessionLocal
from app.repositories.payment_repository import PaymentRepository
from app.services.email_service import send_payment_email
from app.celery_app import celery


@celery.task
def send_payment_email_task(payment_id, status, reason=None):
    db = SessionLocal()

    try:
        repo = PaymentRepository(db)
        payment = repo.find_by_id(payment_id)

        if not payment:
            return

        send_payment_email(payment, status, reason)

    finally:
        db.close()
