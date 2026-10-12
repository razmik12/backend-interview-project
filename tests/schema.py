from pydantic import BaseModel, EmailStr


class UserTestData(BaseModel):
    email: EmailStr
    password: str
    full_name: str
