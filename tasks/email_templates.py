from email.message import EmailMessage

from pydantic import EmailStr

from config.config import settings


def create_message_confirmation_template(key: str, email_to: EmailStr):
    email = EmailMessage()
    email['Subject'] = 'Создание сообщения'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f'''
            <h2>Сообщение создано!</h2>
            <h3>Ваш ключ: {key}</h3>
            <h3>Ваше сообщение автоматически удалится через 30 минут.</h3>
        ''',
        subtype='html',
    )

    return email
