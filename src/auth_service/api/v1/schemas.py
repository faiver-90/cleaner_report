from pydantic import BaseModel, EmailStr, Field


# class JWTCheckInSchema(BaseModel):
#     jwt_code: str | None = None


# class JWTCheckOutSchema(BaseModel):
#     result: bool
class JWTCreateSchema(BaseModel):
    user_id: int
    token: str


class AuthInSchema(BaseModel):
    password: str
    username: str


class AuthOutSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6)


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
