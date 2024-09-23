from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.controller import UserController
from app.api.v1.users.schema.request import UserRoleUpdateRequest, UserCreateCredentials
from app.api.v1.users.schema.response import UserResponse
from core.connections.database_connection import create_session
from core.security import AuthenticationRequired

user_router = APIRouter(prefix="/users", tags=["Users"])

user_controller = UserController()


@user_router.put("/{user_id}/role/", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_slug: UserRoleUpdateRequest,
    db_session: AsyncSession = Depends(create_session),
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await user_controller.update_user_role(
        db_session, user_id, role_slug.role_slug
    )


@user_router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreateCredentials,
    db_session: AsyncSession = Depends(create_session),
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):

    return await user_controller.create(db_session, **user.model_dump())
