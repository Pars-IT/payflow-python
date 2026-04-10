from app.payments.base import PaymentGatewayInterface
from app.payments.result import GatewayResult


class AbnAmroGateway(PaymentGatewayInterface):
    def charge(self, payment):
        if payment.amount % 2 != 0:
            return GatewayResult.failed("abn_amro_rejected")

        return GatewayResult.success()
