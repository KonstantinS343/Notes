import smtplib

from email.message import EmailMessage

from tasks.celery import celery
from src.settings import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from .messages.reset_password_message import message


def email_template(user_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Изменение пароля'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        message.format(token),
        subtype='html'
    )
    return email


@celery.task
def send_email_reset_password_message(user_email: str, token: str):
    email = email_template(user_email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as email_server:
        email_server.login(SMTP_USER, SMTP_PASSWORD)
        email_server.send_message(email)
