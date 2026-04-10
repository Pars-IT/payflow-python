from app.jobs.send_payment_email import send_payment_email_task
from app.events.payment_events import PaymentSucceeded, PaymentFailed
from app.models.payment import Payment


def send_payment_email_listener(event: PaymentSucceeded | PaymentFailed):
    payment: Payment = event.payment

    if isinstance(event, PaymentSucceeded):
        status = "success"
        reason = None
    elif isinstance(event, PaymentFailed):
        status = "failed"
        reason = event.reason
    else:
        raise ValueError(f"Unexpected event type: {type(event)}")

    send_payment_email_task.delay(payment.id, status, reason)
