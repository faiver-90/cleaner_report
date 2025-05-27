from pydantic import BaseModel


class LoginInSchema(BaseModel):
    username: str
    password: str


class LoginOutSchema(BaseModel):
    access_token: str
