from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from core.exception import NotFoundException
from core.models import User, Role, Permission, RolePermission


class PermissionRepository:

    async def create_permission(self, db_session: AsyncSession, **permission_data):
        new_permission = Permission(**permission_data)
        db_session.add(new_permission)
        await db_session.commit()
        return new_permission

    async def get_permission_by_slug(self, db_session, permission_slug):
        permission = (
            await db_session.execute(
                sa.select(Permission).where(Permission.slug == permission_slug)
            )
        ).scalar_one_or_none()

        if not permission:
            raise NotFoundException(error={"message": "مجوزی با این نام یافت نشد"})

        return permission

    async def update_permission(
        self, db_session: AsyncSession, slug: str, **permission_data
    ):
        permission = await self.get_permission_by_slug(db_session, slug)
        for key, value in permission_data.items():
            if hasattr(permission, key):
                setattr(permission, key, value)

        await db_session.commit()
        return permission

    async def delete_permission(self, db_session: AsyncSession, slug: str):
        permission = await self.get_permission_by_slug(db_session, slug)
        await db_session.delete(permission)
        await db_session.commit()

    async def permission_exists(self, db_session, slug):
        return bool(
            (
                await db_session.execute(
                    sa.select(sa.exists().where(Permission.slug == slug))
                )
            ).scalar_one()
        )

    async def get_permissions(self, db_session: AsyncSession):
        permissions = await db_session.execute(sa.select(Permission))
        return permissions.scalars().all()
