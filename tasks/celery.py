from celery import Celery


celery = Celery('executor', broker='redis://localhost:6379/1', include=['tasks.auth.email_verify',
                                                                        'tasks.auth.reset_password'])
