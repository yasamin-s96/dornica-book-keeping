from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.v1.permissions.repository import PermissionRepository
from core.exception import BadRequestException
from core.models import Permission


class PermissionController:
    def __init__(self):
        self.repo = PermissionRepository()

    async def create_permission(self, db_session: AsyncSession, **permission_data):
        if await db_session.scalar(
            sa.select(sa.exists().where(Permission.slug == permission_data["slug"]))
        ):
            raise BadRequestException(error="مجوزی با این نام قبلا وجود دارد")

        return await self.repo.create_permission(db_session, **permission_data)

    async def update_permission(
        self, db_session: AsyncSession, slug: str, **permission_data
    ):
        if "slug" in permission_data and await self.repo.permission_exists(
            db_session, permission_data["slug"]
        ):
            raise BadRequestException(error="مجوزی با این نام قبلا وجود دارد")

        if "slug" in permission_data and "name" in permission_data:
            if permission_data["name"] is None and permission_data["slug"] is None:
                raise BadRequestException(
                    error="حداقل یکی از فیلدهای slug یا name باید پر باشد"
                )

        return await self.repo.update_permission(db_session, slug, **permission_data)

    async def delete_permission(self, db_session: AsyncSession, slug: str):
        try:
            await self.repo.delete_permission(db_session, slug)
        except sa.exc.IntegrityError:
            raise BadRequestException(error="مجوز دارای وابستگیست")

        return {"message": "مجوز با موفقیت حذف شد"}

    async def get_permissions(self, db_session: AsyncSession):
        return await self.repo.get_permissions(db_session)
