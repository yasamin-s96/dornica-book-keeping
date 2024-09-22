from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.roles.repository import RoleRepository
from app.api.v1.users.repository import UserRepository


class UserController:
    def __init__(self):
        self.main_repo = UserRepository()
        self.role_repo = RoleRepository()

    async def update_user_role(
        self, db_session: AsyncSession, user_id: int, new_role_slug: str
    ):
        user = await self.main_repo.get_user(db_session, user_id=user_id)
        new_role = await self.role_repo.get_role_by_slug(db_session, new_role_slug)
        return await self.main_repo.update_user_role(db_session, user, new_role)
