# app/payments/resolver.py

from app.payments.gateways.ideal import IdealGateway
from app.payments.gateways.mollie import MollieGateway
from app.payments.gateways.abn_amro import AbnAmroGateway
from app.payments.gateways.ing import IngGateway


class GatewayResolver:
    def resolve(self, payment):
        if payment.gateway == "mollie":
            return MollieGateway()

        if payment.gateway == "abn-amro":
            return AbnAmroGateway()

        if payment.gateway == "ing":
            return IngGateway()

        return IdealGateway()
