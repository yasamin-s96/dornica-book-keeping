from typing import Annotated
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import AuthenticationRequired
from .controller import PermissionController

from .schema.request import PermissionRequest, PermissionUpdateRequest
from .schema.response import PermissionResponse
from core.connections.database_connection import create_session

permission_router = APIRouter(prefix="/permissions", tags=["Permissions"])

permission_controller = PermissionController()


@permission_router.get("/", response_model=list[PermissionResponse])
async def get_permissions(
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await permission_controller.get_permissions(db_session)


@permission_router.post(
    "/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED
)
async def add_permission(
    permission: PermissionRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await permission_controller.create_permission(
        db_session, **permission.model_dump()
    )


@permission_router.put("/{permission_slug}", response_model=PermissionResponse)
async def update_permission(
    permission_slug: str,
    permission: PermissionUpdateRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await permission_controller.update_permission(
        db_session, permission_slug, **permission.model_dump(exclude_unset=True)
    )


@permission_router.delete("/{permission_slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_slug: str,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await permission_controller.delete_permission(db_session, permission_slug)
