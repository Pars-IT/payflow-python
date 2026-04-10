# app/events/__init__.py
from app.events.event_bus import EventBus
from app.events.payment_events import PaymentSucceeded, PaymentFailed
from app.listeners.reconcile_wallet_listener import reconcile_wallet_listener
from app.listeners.send_payment_email_listener import send_payment_email_listener


def register_events():
    EventBus.subscribe(PaymentSucceeded, send_payment_email_listener)
    EventBus.subscribe(PaymentSucceeded, reconcile_wallet_listener)
    EventBus.subscribe(PaymentFailed, send_payment_email_listener)
