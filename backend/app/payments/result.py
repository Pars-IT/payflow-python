# app/gateways/result.py


class GatewayResult:
    def __init__(
        self, success, reason=None, checkout_url=None, provider_payment_id=None, async_flow=False
    ):
        self.success = success
        self.reason = reason
        self.checkout_url = checkout_url
        self.provider_payment_id = provider_payment_id
        self.async_flow = async_flow

    @staticmethod
    def success():
        return GatewayResult(True)

    @staticmethod
    def failed(reason):
        return GatewayResult(False, reason=reason)

    @staticmethod
    def async_result(provider_payment_id, checkout_url):
        return GatewayResult(
            True,
            checkout_url=checkout_url,
            provider_payment_id=provider_payment_id,
            async_flow=True,
        )
