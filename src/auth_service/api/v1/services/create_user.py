from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas import UserCreateSchema
from repositories.user import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def register_user(self, data: UserCreateSchema):
        existing_user = await self.repo.get_by_email(data.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = pwd_context.hash(data.password)
        return await self.repo.create(data, hashed_password)
