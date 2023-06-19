from functools import lru_cache
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class Setting(BaseSettings):
    class Config:
        env_file: str = ".env"
        case_sensitive: bool = True
    
    PROJECT_NAME: str = "profolio_webserver"
    API_VERSION: str = "/api/v1"
    SMTP_PORT: int = 465
    SMTP_HOST: str = "smtp.gmail.com"
    ALLOWED_CORS_ORIGIN: List[AnyHttpUrl] = [
        AnyHttpUrl("https://abhinasregmi.com.np", scheme="https"),
        AnyHttpUrl("http://127.0.0.1:5500", scheme="http"),
    ]

    # third-parties api endpoint
    ZERO_BOUNCE_VALIDATION_ENDPOINT: AnyHttpUrl = AnyHttpUrl(
        "https://api.zerobounce.in/v2/validate", scheme="https"
    )

    # file upload secret
    FILE_UPLOAD_SECRET: str = "jaynepal"

    # env
    ZERO_BOUNCE_API_KEY: str
    GOOGLE_SMTP_LOGIN: str
    GOOGLE_SMTP_PASS: str
    SENDER_MAIL: str



@lru_cache(maxsize=128)
def get_settings() -> Setting:
    return Setting() #type:ignore


settings = get_settings()