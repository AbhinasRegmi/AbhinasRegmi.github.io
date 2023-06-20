import ssl
import smtplib
from typing import Optional, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import httpx
from jinja2 import Template
from pydantic import EmailStr
from fastapi import UploadFile

from portfolio.app.core.config import settings
from portfolio.app.schemas.email_schema import EmailInputSchema
from portfolio.app.services.exceptions import TryAnotherEmailError, EmailServiceBusyError


class EmailService:
    @classmethod
    async def validate_email(cls, email: EmailStr) -> bool:
        
        params = {
            "email": email,
            "api_key": settings.ZERO_BOUNCE_API_KEY,
            "ip_address": ""
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url = settings.ZERO_BOUNCE_VALIDATION_ENDPOINT,
                params = params
            )

        response_json = response.json()

        if "error" in response_json.keys():
            raise EmailServiceBusyError
        
        try:
            return True if response_json["status"] == "valid" else False
        except KeyError:
            raise TryAnotherEmailError

    @classmethod
    def send_mail_from_client(cls, message: EmailInputSchema) -> None:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
            server.login(settings.GOOGLE_SMTP_LOGIN, settings.GOOGLE_SMTP_PASS)

            final_message = f"""Subject: Message form Portfolio


            FROM: {message.email}
            NAME: {message.name}
            MESSAGE: {message.message}
            """

            server.sendmail(settings.SENDER_MAIL, settings.SENDER_MAIL, final_message)

    @classmethod
    def send_mail_to_client(cls, send_to: EmailStr, template: Template, context: dict, subject: Optional[str] = None) -> None:
        ssl_context = ssl.create_default_context()
    
        rendered_mail = template.render(context)
        body = MIMEText(rendered_mail, "html")
        message = MIMEMultipart()

        if subject:
            message["Subject"] = subject
        message["From"] = settings.SENDER_MAIL
        message["To"] = send_to
        message.attach(payload=body)

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=ssl_context) as server:
            server.login(settings.GOOGLE_SMTP_LOGIN, settings.GOOGLE_SMTP_PASS)

            server.sendmail(settings.SENDER_MAIL, send_to, message.as_string())

    @classmethod
    async def send_mail_attachments(cls, send_to: EmailStr, attachements: List[UploadFile]):
        ssl_context = ssl.create_default_context()

        message = MIMEMultipart()
        message["From"] = settings.SENDER_MAIL
        message["To"] = send_to
        message["Subject"] = "Your file uploads are here."
        message["Message"] = "The server doesn't hold liable for damages. This is just a proxy for attachments."

        for file in attachements:
            file_data = await file.read()
            part = MIMEApplication(file_data)
            part['Content-Disposition'] = f'attachment; filename={file.filename}'
            message.attach(part)

        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=ssl_context) as server:
            server.login(settings.GOOGLE_SMTP_LOGIN, settings.GOOGLE_SMTP_PASS)

            server.sendmail(settings.SENDER_MAIL, send_to, message.as_string())