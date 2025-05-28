import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from api.v1.schemas import (
    LoginInSchema, RegisterInSchema, RegisterOutSchema, TokenResponseSchema
)
from api.v1.services.exceptions_handlers import handle_internal_errors
from api.v1.utils import send_request

logger = logging.getLogger(__name__)
business_logger = logging.getLogger('business')

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'status': 'ok'}


@v1.post('/auth/login', response_model=TokenResponseSchema)
@handle_internal_errors()
async def login(data: LoginInSchema):
    url = "http://auth_service:8001/login"
    payload = data.model_dump()

    business_logger.info(f'User - {data.username}, send request to {url}')
    response = await send_request(method="post", url=url, json=payload)

    response_data = response.json()
    business_logger.info(f'Login response - {response_data}')

    return TokenResponseSchema.model_validate(response_data)


@v1.post('/auth/register', response_model=RegisterOutSchema)
@handle_internal_errors()
async def register(data: RegisterInSchema):
    url = "http://auth_service:8001/register"
    payload = data.model_dump()

    business_logger.info(f'User - {data.username}, send request to {url}')
    response = await send_request(method="post", url=url, json=payload)
    response_data = response.json()

    if response.status_code != 200:
        msg = response_data.get("message", "Unknown error")
        error_type = response_data.get("type")

        logger.error(
            f'Registration failed: {msg} | username: {data.username}, '
            f'email: {data.email}')

        if error_type == "user_already_exists":
            raise HTTPException(status_code=400, detail=msg)

        raise HTTPException(status_code=500, detail=msg)

    business_logger.info(
        f'User registered: username - {data.username}, email - {data.email}')
    return RegisterOutSchema.model_validate(response_data)


@v1.post('/auth/refresh')
@handle_internal_errors()
async def refresh():
    return JSONResponse(content={"status": "not_implemented"}, status_code=501)
