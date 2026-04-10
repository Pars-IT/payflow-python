from app.db import SessionLocal
from app.models.user import User
from app.models.wallet import Wallet
from sqlalchemy.exc import IntegrityError


def seed_wallet():
    session = SessionLocal()
    try:
        user = session.query(User).filter_by(email="habibi.mh@gmail.com").first()
        if not user:
            print("User not found, skipping wallet seed")
            return

        wallet = session.query(Wallet).filter_by(user_id=user.id).first()
        if not wallet:
            wallet = Wallet(
                user_id=user.id,
                balance=0,
            )
            session.add(wallet)
            session.commit()
        else:
            wallet.balance = 0
            session.commit()

        print(f"Wallet seeded for user: {user.email}")
    except IntegrityError as e:
        session.rollback()
        print(f"Error seeding wallet: {e}")
    finally:
        session.close()
