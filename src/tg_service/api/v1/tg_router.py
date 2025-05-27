import logging

from fastapi import APIRouter, HTTPException

from api.v1.schemas import LoginInSchema, RegisterInSchema, RegisterOutSchema
from api.v1.utils import send_request

logger = logging.getLogger(__name__)
business_logger = logging.getLogger('business')

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post('/auth/login')
async def login(data: LoginInSchema):
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


@v1.post('/auth/register', response_model=RegisterOutSchema)
async def register(data: RegisterInSchema):
    username = data.username
    email = data.email
    payload = {
        'username': username,
        'password': data.password,
        'email': email
    }

    business_logger.info(f'User - {username}, send request '
                         f'to http://auth_service:8001/register')
    response = await send_request(
        method="post",
        url="http://auth_service:8001/register",
        json=payload
    )

    response_data = response.json()

    if response.status_code != 200:
        if response_data.get("type") == "user_already_exists":
            logger.error(f'User already exists: '
                         f'\n email - {email}, '
                         f'\n username - {username}')
            raise HTTPException(
                status_code=400,
                detail="User already exists."
            )
        logger.error(f'Unknown error: {response_data.get("message")}'
                     f'\n email - {email}, '
                     f'\n username - {username}')
        raise HTTPException(
            status_code=500,
            detail="Unknown error"
        )

    business_logger.info(f'User registered: username - {username}, '
                         f'email - {email}')

    return RegisterOutSchema.model_validate(response_data)


@v1.post('/auth/refresh')
async def refresh():
    pass
