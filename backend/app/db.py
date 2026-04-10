# app/db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USERNAME}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{settings.DB_DATABASE}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
