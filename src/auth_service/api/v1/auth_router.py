from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas import AuthInSchema, AuthOutSchema, UserOutSchema, \
    UserCreateSchema
from api.v1.services.auth_service import create_access_token, \
    create_refresh_token
from api.v1.services.create_user import UserService
from db.session import get_async_session

v1 = APIRouter()


@v1.get('/')
async def test_connection():
    return {'It\'s': 'Work'}


USERS = {
    'ivan':
        {'username': 'Ivan',
         'password': '123456'}
}


@v1.post("/login", response_model=AuthOutSchema)
def login(data: AuthInSchema):
    user = USERS.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(401, detail="Invalid credentials")

    access = create_access_token(data.username)
    refresh = create_refresh_token(data.username)

    return {"access_token": access, "refresh_token": refresh}


@v1.post("/register", response_model=UserOutSchema)
async def register(
        data: UserCreateSchema,
        db: AsyncSession = Depends(get_async_session)
):
    service = UserService(db)
    try:
        user = await service.register_user(data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @v1.post("/refresh")
# def refresh_token(username: str, refresh_token: str):
#     if not verify_refresh_token(username, refresh_token):
#         raise HTTPException(401, detail="Invalid refresh token")
#
#     access = create_access_token(username)
#     return {"access_token": access}
