from pydantic import BaseModel, EmailStr


class LoginInSchema(BaseModel):
    username: str
    password: str


class LoginOutSchema(BaseModel):
    access_token: str


class RegisterInSchema(LoginInSchema, BaseModel):
    email: EmailStr


class RegisterOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
