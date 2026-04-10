# app/celery_app.py

from functools import lru_cache
from celery import Celery
from app.config import settings
from celery.signals import worker_process_init


@lru_cache
def get_celery() -> Celery:
    celery = Celery(
        "app",
        broker=settings.CELERY_BROKER_URL,
    )

    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
    )

    celery.autodiscover_tasks(["app.jobs"])

    return celery


@worker_process_init.connect
def init_worker(**kwargs):
    from app.events import register_events

    register_events()


celery = get_celery()
