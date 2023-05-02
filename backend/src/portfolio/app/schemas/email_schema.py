from pydantic import BaseModel, EmailStr, Field


class EmailInputSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    message: str = Field(...)