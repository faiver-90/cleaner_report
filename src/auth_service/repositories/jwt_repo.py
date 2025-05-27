from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas import JWTCreateSchema
from db.models import RefreshToken


class JWTRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     jwt_data: JWTCreateSchema):
        jwt = RefreshToken(
            user_id=jwt_data.user_id,
            token=jwt_data.token
        )
        self.session.add(jwt)
        await self.session.commit()
        await self.session.refresh(jwt)
        return jwt
