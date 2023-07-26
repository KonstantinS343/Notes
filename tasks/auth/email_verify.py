import smtplib

from email.message import EmailMessage

from tasks.celery import celery
from src.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, DNS
from .messages.email_verify_message import message


def email_template(user_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Подтверждение регистрации'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        message.format(DNS, token, DNS, token),
        subtype='html'
    )
    return email


@celery.task
def send_email_verify_message(user_email: str, token: str):
    email = email_template(user_email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as email_server:
        email_server.login(SMTP_USER, SMTP_PASSWORD)
        email_server.send_message(email)
