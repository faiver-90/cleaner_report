from fastapi import APIRouter, HTTPException, Depends

from api.v1.schemas import AuthInSchema, AuthOutSchema
from api.v1.services.auth_service import create_access_token, \
    create_refresh_token

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

# @v1.post("/refresh")
# def refresh_token(username: str, refresh_token: str):
#     if not verify_refresh_token(username, refresh_token):
#         raise HTTPException(401, detail="Invalid refresh token")
#
#     access = create_access_token(username)
#     return {"access_token": access}
