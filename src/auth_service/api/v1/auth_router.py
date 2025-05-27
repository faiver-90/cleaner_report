from fastapi import APIRouter, Depends

import jwt
from api.v1.schemas import JWTCheckInSchema

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post('/check_jwt')
async def auth(data: JWTCheckInSchema):
    return {'jwt': data.jwt_code}
