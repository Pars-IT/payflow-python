# app/payments/gateways/ideal.py

from app.payments.base import PaymentGatewayInterface
from app.payments.result import GatewayResult


class IdealGateway(PaymentGatewayInterface):
    def charge(self, payment):
        if payment.amount < 1000:
            return GatewayResult.failed("amount_too_low")

        return GatewayResult.success()
