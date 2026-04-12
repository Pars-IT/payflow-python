# app/payments/gateways/mollie.py
import requests
from app.payments.base import PaymentGatewayInterface
from app.payments.result import GatewayResult
from app.config import settings
from app.models.payment import Payment
from app.exceptions.psp_exception import PspException


class MollieGateway(PaymentGatewayInterface):
    def charge(self, payment: Payment) -> GatewayResult:
        """
        Charge the payment via Mollie API and return GatewayResult.
        """
        try:
            headers = {
                "Authorization": f"Bearer {settings.MOLLIE_API_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "amount": {
                    "currency": "EUR",
                    "value": f"{payment.amount / 100:.2f}",
                },
                "description": f"Payment #{payment.id}",
                "redirectUrl": f"{settings.APP_URL}/payments/{payment.id}",
                "webhookUrl": f"{settings.APP_URL}/api/webhooks/mollie",
                "method": "ideal",
                "metadata": {"payment_id": payment.id},
            }

            response = requests.post(
                "https://api.mollie.com/v2/payments", headers=headers, json=payload
            )
            response.raise_for_status()  # HTTP errors => exception

            data = response.json()

            return GatewayResult.async_result(
                provider_payment_id=data["id"],
                checkout_url=data["_links"]["checkout"]["href"],
            )

        except requests.RequestException as e:
            msg = str(e)
            if "amount" in msg.lower():
                reason = "psp_invalid_amount"
            elif "webhook" in msg.lower():
                reason = "psp_webhook_unreachable"
            else:
                reason = "psp_error"

            raise PspException(reason)
