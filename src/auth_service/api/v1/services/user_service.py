from api.v1.configs.crypt_conf import pwd_context
from api.v1.schemas import UserCreateSchema


class UserService:
    def __init__(self, repo):
        self.repo = repo

    async def register_user(self, data: UserCreateSchema):
        existing_user = await self.repo.exists_by_fields(
            email=data.email,
            username=data.username)
        if existing_user:
            raise ValueError("User with this email or username already exists")

        hashed_password = pwd_context.hash(data.password)
        return await self.repo.create(data, hashed_password)
