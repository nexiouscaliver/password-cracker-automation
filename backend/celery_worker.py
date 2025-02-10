# celery_worker.py
from celery import Celery
from config import Config

def make_celery(app_name=__name__):
    return Celery(app_name, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

celery = make_celery()

if __name__ == '__main__':
    celery.start()
