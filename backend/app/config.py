# app/config.py

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Payment"
    APP_ENV: str = "local"
    APP_DEBUG: bool = True
    APP_URL: str

    # DB
    DB_HOST: str
    DB_PORT: int = 3306
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Mollie
    MOLLIE_API_KEY: str
    MOLLIE_WEBHOOK_SECRET: str

    # Task Queue
    CELERY_BROKER_URL: str

    # Mail
    MAIL_MAILER: str = "smtp"
    MAIL_HOST: str
    MAIL_PORT: int = 587
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_ENCRYPTION: str = "tls"
    MAIL_FROM_ADDRESS: str
    MAIL_FROM_NAME: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()
