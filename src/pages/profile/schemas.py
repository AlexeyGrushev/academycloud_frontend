from pydantic import BaseModel, EmailStr, Field


class SUpdateUser(BaseModel):
    email: EmailStr | None = Field(default=None)
    login: str | None = Field(default=None)
    password: str | None = Field(default=None, min_length=8)
