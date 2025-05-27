import json
import logging

from fastapi import APIRouter, HTTPException, Depends, Body

from api.v1.configs.exceptions_handlers import handle_internal_errors
from api.v1.schemas import LoginInSchema
from api.v1.utils import send_request

logger = logging.getLogger(__name__)
business_logger = logging.getLogger('business')

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post('/auth/login')
@handle_internal_errors()
async def login(data: LoginInSchema):
    print(data)
    payload = {
        'username': data.username,
        'password': data.password
    }

    business_logger.info(f'User - {data.username}, send request '
                         f'to http://auth_service:8001/login')
    response = await send_request(
        method="post",
        url="http://auth_service:8001/login",
        json=payload
    )

    response_data = response.json()
    access_token = response_data.get("access_token")

    business_logger.info(f'User - {data.username}, get '
                         f'access_token: {access_token}')
    return {"access_token": access_token}


@v1.post('/auth/refresh')
async def refresh():
    pass
