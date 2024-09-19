import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from jose import jwt

from settings import settings


def generate_email_token(user_email: str, payload: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.email_token_expire_time)
    payload.update({"exp": expire})
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

    return token


def send_email(subject: str, recipient: str, body: str):
    sender_email = settings.email_host_user
    password = settings.email_host_password

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient

    with smtplib.SMTP(settings.email_host, int(settings.email_port)) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message.as_string())


def send_email_verification_link(user_email: str):
    payload = {"email": user_email}
    verification_token = generate_email_token(user_email, payload)

    base_url = f"http://{settings.app_host}:{settings.app_port}"
    verification_link = (
        f"{base_url}/api/v1/auth/verify-email?token={verification_token}"
    )

    recipient = user_email
    subject = "تایید آدرس ایمیل"
    body = f"برای تایید آدرس ایمیل خود، کلیک کنید: {verification_link}"

    send_email(recipient=recipient, subject=subject, body=body)


def send_reset_password_link(user_email: str):
    payload = {"forgot_password_email": user_email}
    reset_token = generate_email_token(user_email, payload)

    base_url = f"http://{settings.app_host}:{settings.app_port}"
    reset_link = f"{base_url}/api/v1/auth/reset-password?token={reset_token}"

    recipient = user_email
    subject = "بازیابی کلمه عبور"
    body = f"برای بازیابی کلمه عبور خود، کلیک کنید: {reset_link}"

    send_email(recipient=recipient, subject=subject, body=body)
