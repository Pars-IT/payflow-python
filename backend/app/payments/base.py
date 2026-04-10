# app/gateways/base.py

from abc import ABC, abstractmethod


class PaymentGatewayInterface(ABC):
    @abstractmethod
    def charge(self, payment):
        pass
