from app.jobs.reconcile_wallet import reconcile_wallet_task


def reconcile_wallet_listener(event):
    payment = event.payment
    reconcile_wallet_task.delay(payment.id)
