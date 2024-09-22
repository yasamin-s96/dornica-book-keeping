from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.v1.permissions.repository import PermissionRepository
from app.api.v1.role_permissions.repository import RolePermissionRepository
from app.api.v1.roles.repository import RoleRepository
from core.exception import NotFoundException, BadRequestException
from core.models import User, Role, Permission, RolePermission


class RolePermissionController:
    def __init__(self):
        self.main_repo = RolePermissionRepository()
        self.permission_repo = PermissionRepository()
        self.role_repo = RoleRepository()

    async def assign_permission_to_role(
        self, db_session: AsyncSession, role_slug: str, permission_slug: str
    ):
        role = await self.role_repo.get_role_by_slug(db_session, role_slug)
        permission = await self.permission_repo.get_permission_by_slug(
            db_session, permission_slug
        )
        role_permission_exists = await self.main_repo.role_permission_exists(
            db_session, role.id, permission.id
        )
        if role_permission_exists:
            raise BadRequestException(error="دسترسی از قبل موجود است")

        return await self.main_repo.assign_permission_to_role(
            db_session, role.id, permission.id
        )

    async def delete_role_permission(
        self, db_session: AsyncSession, role_slug: str, permission_slug: str
    ):
        role = await self.role_repo.get_role_by_slug(db_session, role_slug)
        permission = await self.permission_repo.get_permission_by_slug(
            db_session, permission_slug
        )

        return await self.main_repo.delete_role_permission(
            db_session, role.id, permission.id
        )

    async def get_role_permissions(self, db_session: AsyncSession):
        return await self.main_repo.get_role_permissions(db_session)
