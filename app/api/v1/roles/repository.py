from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from core.exception import NotFoundException
from core.models import User, Role, Permission, RolePermission


class RoleRepository:

    async def create_role(self, db_session: AsyncSession, **role_data):
        new_role = Role(**role_data)
        db_session.add(new_role)
        await db_session.commit()
        return new_role

    async def get_roles(self, db_session: AsyncSession):
        return (await db_session.execute(sa.select(Role))).scalars().all()

    async def update_role(self, db_session: AsyncSession, role_slug: str, **role_data):
        role = await self.get_role_by_slug(db_session, role_slug)
        for key, value in role_data.items():
            setattr(role, key, value)

        await db_session.commit()
        await db_session.refresh(role)
        return role

    async def delete_role(self, db_session: AsyncSession, role_slug: str):
        role = await self.get_role_by_slug(db_session, role_slug)
        await db_session.delete(role)
        await db_session.commit()

        return {"message": "نقش با موفقیت حذف شد"}

    async def get_role_by_slug(self, db_session: AsyncSession, role: str):
        role = (
            await db_session.execute(sa.select(Role).where(Role.slug == role))
        ).scalar_one_or_none()

        if not role:
            raise NotFoundException(error={"message": "نقشی با این نام یافت نشد"})

        return role

    async def get_role_by_id(self, db_session: AsyncSession, role_id: int):
        role = (
            await db_session.execute(sa.select(Role).where(Role.id == role_id))
        ).scalar_one_or_none()

        if not role:
            raise NotFoundException(error={"message": "نقشی برای این نام یافت نشد"})

        return role

    async def get_role_permissions_by_slug(
        self, db_session: AsyncSession, role_slug: str
    ):
        query = (
            sa.select(Permission.slug)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(Role, RolePermission.role_id == Role.id)
            .where(Role.slug == role_slug)
        )
        user_permissions = (await db_session.execute(query)).scalars().all()
        user_permissions = [str(permission) for permission in user_permissions]

        if not user_permissions:
            raise NotFoundException(error={"message": "مجوزی برای این نقش یافت نشد"})
        return user_permissions

    async def role_exists(self, db_session: AsyncSession, slug: str):
        return bool(
            (
                await db_session.execute(
                    sa.select(sa.exists().where(Role.slug == slug))
                )
            ).scalar_one()
        )
