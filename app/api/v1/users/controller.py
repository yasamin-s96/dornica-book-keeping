from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.roles.repository import RoleRepository
from app.api.v1.users.repository import UserRepository
from core.exception import BadRequestException


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

    async def create(self, db_session: AsyncSession, **credentials):
        email = credentials.get("email")
        if await self.main_repo.email_exists(db_session, email):
            raise BadRequestException(
                message="کاربر با ایمیل وارد شده از قبل وجود دارد"
            )
        role = await self.role_repo.get_role_by_slug(db_session, credentials["role"])
        credentials.update({"role_id": role.id})
        return await self.main_repo.admin_create(db_session, **credentials)
