from sqlalchemy.ext.asyncio import AsyncSession
from .schema.request import AllowedIP
from .repository import IPRepository
from ..users.repository import UserRepository


class IPController:
    def __init__(self):
        self.repo = IPRepository()
        self.user_repo = UserRepository()

    async def store_allowed_ips(
        self, db_session: AsyncSession, user_id: int, allowed_ips: list[AllowedIP]
    ):
        await self.user_repo.get_user(db_session, user_id=user_id)
        return await self.repo.store_allowed_ips(db_session, user_id, allowed_ips)

    async def allowed_ips(self, db_session: AsyncSession, user_id: int):
        await self.user_repo.get_user(db_session, user_id=user_id)
        return await self.repo.get_allowed_ips(db_session, user_id)
