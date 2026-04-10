# app/jobs/reconcile_wallet.py
from app.celery_app import celery


@celery.task
def reconcile_wallet_task(payment_id):
    print(f"[RECONCILE] payment={payment_id}")
