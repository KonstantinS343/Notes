from celery import Celery

from src.settings import CELERY_HOST, CELERY_PORT


celery = Celery('executor', broker=f'redis://{CELERY_HOST}:{CELERY_PORT}', include=['tasks.auth.email_verify',
                                                                                    'tasks.auth.reset_password'])
