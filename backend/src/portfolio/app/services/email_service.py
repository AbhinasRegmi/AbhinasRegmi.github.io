import ssl
import smtplib

import httpx
from pydantic import EmailStr

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
    async def send_mail_to_client(cls) -> None:
        import time
        time.sleep(5)