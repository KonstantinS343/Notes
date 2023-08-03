import smtplib

from email.message import EmailMessage

from tasks.celery import celery
from src.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from .messages.delete_notification_message import message


def email_template(user_email: str):
    email = EmailMessage()
    email['Subject'] = 'Удаление аккаунта'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        message,
        subtype='html'
    )
    return email


@celery.task
def send_email_delete_notification(user_email: str):
    email = email_template(user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as email_server:
        email_server.login(SMTP_USER, SMTP_PASSWORD)
        email_server.send_message(email)
