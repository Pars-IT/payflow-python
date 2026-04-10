"""init

Revision ID: f77d408bdc98
Revises:
Create Date: 2026-04-07 18:44:39.793995

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f77d408bdc98"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # -------------------- users --------------------
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("email_verified_at", sa.DateTime(), nullable=True),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("remember_token", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    # -------------------- wallets --------------------
    op.create_table(
        "wallets",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger, nullable=False),
        sa.Column("balance", sa.BigInteger, server_default="0", nullable=False),
        sa.Column("currency", sa.CHAR(3), server_default="EUR", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    # -------------------- payments --------------------
    op.create_table(
        "payments",
        sa.Column("id", sa.String(36), primary_key=True),  # UUID
        sa.Column("gateway", sa.String(50), server_default="ideal", nullable=False),
        sa.Column("provider", sa.String(100), nullable=True),
        sa.Column("provider_payment_id", sa.String(100), nullable=True),
        sa.Column("provider_checkout_url", sa.Text(), nullable=True),
        sa.Column("user_id", sa.BigInteger, nullable=False),
        sa.Column("amount", sa.BigInteger, nullable=False),
        sa.Column("currency", sa.CHAR(3), server_default="EUR", nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "success", "failed", name="payment_status"),
            nullable=False,
        ),
        sa.Column("failure_reason", sa.String(255), nullable=True),
        sa.Column("idempotency_key", sa.String(255), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("provider", "provider_payment_id", name="provider_payment_unique"),
    )

    op.create_index("ix_payments_status", "payments", ["status"])
    op.create_index("idx_user_status", "payments", ["user_id", "status"])

    # -------------------- transactions --------------------
    op.create_table(
        "transactions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("wallet_id", sa.BigInteger, nullable=False),
        sa.Column("payment_id", sa.String(36), nullable=True, unique=True),
        sa.Column("amount", sa.BigInteger, nullable=False),
        sa.Column(
            "type",
            sa.Enum("credit", "debit", name="transaction_type"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["wallet_id"], ["wallets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["payment_id"], ["payments.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("transactions")
    op.drop_index("idx_user_status", table_name="payments")
    op.drop_index("ix_payments_status", table_name="payments")
    op.drop_table("payments")
    op.drop_table("wallets")
    op.drop_table("users")
