import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str
):
    message = MIMEMultipart()
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD
        )

        server.send_message(message)

def send_payment_confirmation_email(
    participant_email: str,
    participant_name: str,
    workshop_name: str,
    workshop_datetime: str,
    registration_id: int,
    payment_status: str
):
    subject = "Workshop Registration Confirmed"

    body = f"""
Hello {participant_name},

Your workshop registration has been confirmed successfully.

Workshop: {workshop_name}
Date & Time: {workshop_datetime}
Registration ID: {registration_id}
Payment Status: {payment_status}

Thank you for registering.

Event Workshop System
"""

    send_email(
        to_email=participant_email,
        subject=subject,
        body=body
    )

def send_cancellation_email(
    participant_email: str,
    participant_name: str,
    workshop_name: str,
    registration_id: int
):
    subject = "Workshop Registration Cancelled"

    body = f"""
Hello {participant_name},

Your workshop registration has been cancelled.

Workshop: {workshop_name}
Registration ID: {registration_id}
Status: CANCELLED

Thank you.

Event Workshop System
"""

    send_email(
        to_email=participant_email,
        subject=subject,
        body=body
    )    