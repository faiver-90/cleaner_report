from fastapi import APIRouter, Body

from api.v1.schemas import JWTInSchema
import api.v1.configs.log_conf

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post('/check_jwt')
async def check_jwt(data: JWTInSchema):
    print(data.code)
    return {'jwt': data.code}
