from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core.connections.database_connection import create_session
from core.security.check_auth import AuthenticationRequired
from .controller import IPController
from .schema.request import AllowedIP


ip_router = APIRouter(prefix="/allowed-ips", tags=["Allowed IPs"])

ip_controller = IPController()


@ip_router.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
async def store_allowed_ips(
    user_id: int,
    allowed_ips: list[AllowedIP],
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(AuthenticationRequired.check_auth, scopes=["admin"]),
):
    return await ip_controller.store_allowed_ips(db_session, user_id, allowed_ips)
