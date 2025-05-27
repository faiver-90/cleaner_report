from pydantic import BaseModel


class JWTCheckInSchema(BaseModel):
    jwt_code: str | None = None


class JWTCheckOutSchema(BaseModel):
    result: bool


class AuthInSchema(BaseModel):
    password: str
    username: str


class AuthOutSchema(BaseModel):
    token: str
