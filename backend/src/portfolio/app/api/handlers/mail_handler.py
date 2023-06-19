from typing import List

from pydantic import EmailStr
from fastapi import APIRouter, status, BackgroundTasks, Body, UploadFile


from portfolio.app.core.config import settings
from portfolio.app.services.email_service import EmailService
from portfolio.app.schemas.template_schema import HTMLTemplate
from portfolio.app.schemas.email_schema import EmailInputSchema
from portfolio.app.api.handlers.exceptions import InvalidEmailError
from portfolio.app.api.handlers.exceptions import UploadSecretInvalidError

mail_router = APIRouter(prefix="/mail", tags=["mail"])


@mail_router.post("/send", status_code=status.HTTP_200_OK)
async def send_email(background_tasks: BackgroundTasks, message: EmailInputSchema = Body(...)):
    response = await EmailService.validate_email(message.email)

    if not response:
        return {
            "msg": "Try again with Correct Email."
        }
    
    background_tasks.add_task(
        EmailService.send_mail_from_client,
        message
    )
    background_tasks.add_task(
        EmailService.send_mail_to_client,
        message.email,
        HTMLTemplate.THANKYOU,
        {"name": message.name},
        "Get Back To You Soon."
    )

    return {
        "msg": "OK"
    }


@mail_router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile], send_to: EmailStr = Body(...), secret: str = Body(...)):
    if not secret == settings.FILE_UPLOAD_SECRET:
        raise UploadSecretInvalidError
    
    response = await EmailService.validate_email(send_to)
    if not response:
        raise InvalidEmailError
    
    background_tasks.add_task(
        EmailService.send_mail_attachments,
        send_to,
        files
    )

    return {
        "msg": "OK"
    }
    
