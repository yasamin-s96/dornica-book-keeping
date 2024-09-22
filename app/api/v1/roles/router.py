from typing import Annotated
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import AuthenticationRequired
from .controller import RoleController

from .schema.request import RoleRequest, RoleUpdateRequest
from .schema.response import RoleResponse
from core.connections.database_connection import create_session

role_router = APIRouter(prefix="/roles", tags=["Roles"])

role_controller = RoleController()


@role_router.get("/", response_model=list[RoleResponse])
async def get_roles(
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_controller.get_roles(db_session)


@role_router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def add_role(
    role: RoleRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_controller.create_role(db_session, **role.model_dump())


@role_router.put("/{role_slug}", response_model=RoleResponse)
async def update_role(
    role_slug: str,
    role: RoleUpdateRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_controller.update_role(
        db_session, role_slug, **role.model_dump(exclude_unset=True)
    )


@role_router.delete("/{role_slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_slug: str,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await role_controller.delete_role(db_session, role_slug)
