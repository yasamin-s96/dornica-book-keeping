from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from core.exception import BadRequestException
from .repository import RoleRepository


class RoleController:
    def __init__(self):
        self.repo = RoleRepository()

    async def create_role(self, db_session: AsyncSession, **role_data):
        slug = role_data.get("slug")
        if await self.repo.role_exists(db_session, slug):
            raise BadRequestException(error="نقشی با این نام وجود دارد")
        return await self.repo.create_role(db_session, **role_data)

    async def get_roles(self, db_session: AsyncSession):
        return await self.repo.get_roles(db_session)

    async def update_role(self, db_session: AsyncSession, role_slug: str, **role_data):
        if "slug" in role_data and await self.repo.role_exists(
            db_session, role_data["slug"]
        ):
            raise BadRequestException(error="نقشی با این نام وجود دارد")

        if "slug" in role_data and "name" in role_data:
            if role_data["name"] is None and role_data["slug"] is None:
                raise BadRequestException(
                    error="حداقل یکی از فیلدهای slug یا name باید پر باشد"
                )

        return await self.repo.update_role(db_session, role_slug, **role_data)

    async def delete_role(self, db_session: AsyncSession, role_slug: str):
        try:
            await self.repo.delete_role(db_session, role_slug)
        except sa.exc.IntegrityError:
            raise BadRequestException(error="نقش دارای وابستگیست")

        return {"message": "نقش با موفقیت حذف شد"}
