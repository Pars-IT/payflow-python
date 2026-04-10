# app/models/base.py
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.sql import func
from datetime import datetime, timezone

Base = declarative_base()


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            server_default=func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            default=datetime.now(timezone.utc),
            onupdate=datetime.now(timezone.utc),
            server_default=func.now(),
            nullable=False,
        )
