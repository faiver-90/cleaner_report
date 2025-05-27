import logging

from api.v1.configs.crypt_conf import pwd_context
from api.v1.schemas import JWTCreateSchema
from api.v1.services.jwt_service import create_access_token, \
    create_refresh_token
from repositories.jwt_repo import JWTRepo
from repositories.user_repo import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepository, jwt_repo: JWTRepo):
        self.user_repo = user_repo
        self.jwt_repo = jwt_repo

    async def login(self, username: str, password: str):
        user = await self.user_repo.get_by_fields(username=username)
        if not user:
            logger.error(f'Invalid username or password. Username - '
                         f'{username}')
            raise ValueError("Invalid username or password")

        if not pwd_context.verify(password, user.hashed_password):
            logger.error(f'Invalid username or password. Username - '
                         f'{username}')
            raise ValueError("Invalid username or password")

        access = create_access_token(user.username)
        refresh = create_refresh_token(user.username)

        await self.jwt_repo.create(JWTCreateSchema(user_id=user.id,
                                                   token=refresh))

        return {"access_token": access, "refresh_token": refresh}
