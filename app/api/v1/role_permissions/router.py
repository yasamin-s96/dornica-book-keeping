from typing import Annotated
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import AuthenticationRequired
from .controller import RolePermissionController

from .schema.request import RolePermissionRequest
from .schema.response import RolePermissionResponse
from core.connections.database_connection import create_session

role_permission_router = APIRouter(
    prefix="/role-permissions", tags=["Role Permissions"]
)

role_permission_controller = RolePermissionController()


@role_permission_router.get("/", response_model=list[RolePermissionResponse])
async def get_role_permissions(
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_permission_controller.get_role_permissions(db_session)


@role_permission_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_permission(
    role_permission: RolePermissionRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_permission_controller.assign_permission_to_role(
        db_session, role_permission.role_slug, role_permission.permission_slug
    )


@role_permission_router.delete(
    "/{role_slug}/{permission_slug}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_permission(
    role_slug: str,
    permission_slug: str,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_permission_controller.delete_role_permission(
        db_session, role_slug, permission_slug
    )
