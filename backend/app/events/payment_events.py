class PaymentSucceeded:
    def __init__(self, payment):
        self.payment = payment


class PaymentFailed:
    def __init__(self, payment, reason):
        self.payment = payment
        self.reason = reason
