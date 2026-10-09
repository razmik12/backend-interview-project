import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    email: EmailStr
    full_name: str
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshPayload(BaseModel):
    sub: uuid.UUID
    session_id: uuid.UUID
    type: str = "refresh_token"


class UserTestData(BaseModel):
    email: EmailStr
    full_name: str
    password: str
