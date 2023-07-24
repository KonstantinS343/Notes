import smtplib

from email.message import EmailMessage

from tasks.celery import celery
from src.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from .messages.email_verify_message import message


def email_template():
    email = EmailMessage()
    email['Subject'] = 'Подтверждение регистрации'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        message,
        subtype='html'
    )
    return email


@celery.task
def send_email_verify_message():
    email = email_template()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as email_server:
        email_server.login(SMTP_USER, SMTP_PASSWORD)
        email_server.send_message(email)
