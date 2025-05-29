from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginInSchema(BaseModel):
    username: str
    password: str


class RegisterInSchema(LoginInSchema, BaseModel):
    email: EmailStr


class RegisterOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool

    class Config:
        orm_mode = True


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserOutSchema
