import logging

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from api.v1.schemas import AuthInSchema, UserOutSchema, UserCreateSchema, \
    TokenResponseSchema
from api.v1.services.auth_service import AuthService

from api.v1.services.exceptions_handlers import handle_internal_errors
from api.v1.services.user_service import UserService
from db.session import get_async_session

from repositories.jwt_repo import JWTRepo
from repositories.user_repo import UserRepository

v1 = APIRouter()

logger = logging.getLogger(__name__)
business_logger = logging.getLogger('business')


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


@v1.post("/login", response_model=TokenResponseSchema)
@handle_internal_errors()
async def login(token_data: AuthInSchema,
                db: AsyncSession = Depends(get_async_session)):
    service = AuthService(UserRepository(db), JWTRepo(db))
    username = token_data.username

    try:
        business_logger.info(f'Login request. Username - {username}')
        token_data = await service.login(username, token_data.password)

        return token_data
    except ValueError as e:
        logger.error(f'Invalid credentials. Username - {username}')
        return JSONResponse(
            status_code=401,
            content={
                "status": "error",
                "message": f"Invalid credentials - {e}"
            }
        )


@v1.post("/register", response_model=UserOutSchema)
@handle_internal_errors()
async def register(
        data: UserCreateSchema,
        db: AsyncSession = Depends(get_async_session)):
    service = UserService(UserRepository(db))
    try:

        user = await service.register_user(data)

        return user
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "type": "user_already_exists",
                "message": str(e)
            }
        )
