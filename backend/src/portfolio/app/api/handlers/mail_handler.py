from fastapi import APIRouter, status, BackgroundTasks, Body

from portfolio.app.services.email_service import EmailService
from portfolio.app.schemas.template_schema import HTMLTemplate
from portfolio.app.schemas.email_schema import EmailInputSchema

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