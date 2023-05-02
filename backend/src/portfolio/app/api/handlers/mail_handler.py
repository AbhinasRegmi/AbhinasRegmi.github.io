from fastapi import APIRouter, status, BackgroundTasks, Body

from portfolio.app.services.email_service import EmailService
from portfolio.app.services.exceptions import InvalidEmailError
from portfolio.app.schemas.email_schema import EmailInputSchema

mail_router = APIRouter(prefix="/mail", tags=["mail"])


@mail_router.post("/send", status_code=status.HTTP_200_OK)
async def send_email(background_tasks: BackgroundTasks, message: EmailInputSchema = Body(...)):
    response = await EmailService.validate_email(message.email)

    if not response:
        raise InvalidEmailError
    
    background_tasks.add_task(EmailService.send_mail_from_client, message)
    background_tasks.add_task(EmailService.send_mail_to_client)

    return {
        "message": "Your email was sent."
    }
    
