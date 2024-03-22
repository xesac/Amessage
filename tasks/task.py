import smtplib

from pydantic import EmailStr

from config.config import settings
from tasks.celery_app import celery
from tasks.email_templates import create_message_confirmation_template


@celery.task
def send_message_confirmation_email(key: str, email_to: EmailStr):
    msg_content = create_message_confirmation_template(key, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
