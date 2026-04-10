# app/payments/gateways/ideal.py

from app.payments.base import PaymentGatewayInterface
from app.payments.result import GatewayResult


class IngGateway(PaymentGatewayInterface):
    def charge(self, payment):
        # Test: Always successful
        return GatewayResult.success()
