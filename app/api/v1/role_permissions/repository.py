from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.v1.role_permissions.schema.response import RolePermissionResponse
from core.exception import NotFoundException
from core.models import User, Role, Permission, RolePermission


class RolePermissionRepository:

    async def assign_permission_to_role(
        self, db_session: AsyncSession, role_id: int, permission_id: int
    ):
        new_role_permission = RolePermission(
            role_id=role_id, permission_id=permission_id
        )
        db_session.add(new_role_permission)
        await db_session.commit()
        await db_session.refresh(new_role_permission)
        return new_role_permission

    async def get_role_permissions(self, db_session: AsyncSession):
        query = (
            sa.select(Role.slug.label("role"), Permission.slug.label("permission"))
            .select_from(RolePermission)
            .join(Role, RolePermission.role_id == Role.id)
            .join(Permission, RolePermission.permission_id == Permission.id)
        )
        result = (await db_session.execute(query)).fetchall()

        response = [
            RolePermissionResponse(role_slug=row[0], permission_slug=row[1])
            for row in result
        ]

        return response

    async def role_permission_exists(
        self, db_session: AsyncSession, role_id: int, permission_id: int
    ):
        role_permission = bool(
            (
                await db_session.execute(
                    sa.select(
                        sa.exists(RolePermission.role_id).where(
                            RolePermission.role_id == role_id,
                            RolePermission.permission_id == permission_id,
                        )
                    )
                )
            ).scalar_one()
        )

        return role_permission

    async def delete_role_permission(
        self, db_session, role_id: int, permission_id: int
    ):
        query = sa.delete(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        await db_session.execute(query)
        await db_session.commit()

        return {"message": "مجوز با موفقیت حذف شد"}

    async def get_role_permissions_by_role_slug(
        self, db_session: AsyncSession, role_slug
    ):
        query = (
            sa.select(Permission.slug)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(Role, RolePermission.role_id == Role.id)
            .where(Role.slug == role_slug)
        )
        result = (await db_session.execute(query)).fetchall()

        permissions = [permission[0] for permission in result]

        return permissions
