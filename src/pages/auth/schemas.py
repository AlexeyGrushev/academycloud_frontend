from pydantic import BaseModel, EmailStr, Field


class SEmail(BaseModel):
    email: EmailStr


class SPassword(BaseModel):
    password: str = Field(min_length=8)
