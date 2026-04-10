# app/api/wallet.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import SessionLocal
from app.models.wallet import Wallet

router = APIRouter()


# --- Pydantic Response Model ---
class WalletResponse(BaseModel):
    user_id: int
    balance: int


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoint ---
@router.get(
    "/wallets/{user_id}",
    summary="Get Wallet Balance",
    description="""
Returns the current wallet balance for a specific user.

**Purpose:**
- Allow users to see their available balance
- Useful for frontend wallet dashboards
- Can be used to validate if enough funds exist before purchases

**Path Parameters:**
- `user_id`: ID of the user

**Response:**
- `user_id`: The requested user's ID
- `balance`: Current balance in cents
""",
    response_model=WalletResponse,
)
def get_wallet(user_id: int, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

    if not wallet:
        return WalletResponse(user_id=user_id, balance=0)

    return WalletResponse(user_id=user_id, balance=wallet.balance)
