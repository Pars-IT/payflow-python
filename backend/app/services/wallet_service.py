# app/services/wallet_service.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.wallet import Wallet
from app.models.transaction import Transaction


class WalletService:
    def __init__(self, db: Session):
        self.db = db

    def credit_from_payment(self, payment):
        try:
            # start transaction
            wallet = self.db.execute(
                select(Wallet)
                .where(Wallet.user_id == payment.user_id)
                .with_for_update()  # equal to lockForUpdate
            ).scalar_one_or_none()

            if not wallet:
                raise Exception("wallet_not_found")

            tx = Transaction(
                wallet_id=wallet.id, payment_id=payment.id, amount=payment.amount, type="credit"
            )

            self.db.add(tx)

            wallet.balance += payment.amount

            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e
