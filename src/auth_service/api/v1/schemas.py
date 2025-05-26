from pydantic import BaseModel


class JWTInSchema(BaseModel):
    code: str
