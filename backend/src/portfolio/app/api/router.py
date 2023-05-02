from fastapi import APIRouter

from portfolio.app.core.config import settings
from portfolio.app.api.handlers import mail_handler

router = APIRouter(
    prefix=settings.API_VERSION
)


router.include_router(mail_handler.mail_router)

