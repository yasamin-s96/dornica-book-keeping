from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from typing import Annotated

from core.security import JWTHandler
from core.connections.redis import whitelist, blacklist
from core.connections.database_connection import async_session
from core.exception.base import AuthenticationRequiredException, ForbiddenException


class AuthenticationRequired:
    @staticmethod
    async def check_auth(
        req: Request,
        scopes: SecurityScopes,
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))
        ],
    ):
        if not credentials:
            raise AuthenticationRequiredException(error="نیاز به احراز هویت دارید")
        token = credentials.credentials
        payload = JWTHandler.decode(token)
        if not token:
            raise ForbiddenException(error="توکن نامعتبر است")

        client_ip = req.client.host
        token_ip = payload.get("ip")
        ip_check = payload.get("ip_check")
        user_scope = payload.get("scope")
        current_permissions = payload.get("permissions")
        database_permissions = await AuthenticationRequired.get_role_permissions(
            role=user_scope
        )

        # Check if user has the required permission
        if scopes and user_scope not in scopes.scopes:
            raise ForbiddenException()

        # Revoke token if permissions have changed
        if set(current_permissions) != set(database_permissions):
            whitelist.delete(token)
            raise AuthenticationRequiredException(
                error="سطح دسترسی تغییر یافت. دوباره وارد شوید"
            )

        # Check if IP is backlisted
        banned = blacklist.get(f"blacklist:{client_ip}")
        if banned:
            raise ForbiddenException(error="دسترسی شما به سرویس مسدود شده است")

        # Check if client IP matches token IP
        if client_ip != token_ip:
            raise ForbiddenException(error="عدم تطابق آی پی")

        # Exist in whitelist
        if not whitelist.get(token):
            raise AuthenticationRequiredException(error="نیاز به احراز هویت دارید")

        # Check if IP check is enabled and client IP matches with user's allowed IPs
        if ip_check:
            user_allowed_ips = await AuthenticationRequired.get_allowed_ips(
                payload.get("user_id")
            )
            if client_ip not in user_allowed_ips:
                raise ForbiddenException(error="عدم تطابق آی پی")

        return payload

    @staticmethod
    async def get_current_user_id(
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))
        ],
    ):
        token = credentials.credentials
        payload = JWTHandler.decode(token)
        return payload.get("user_id")

    @staticmethod
    async def get_allowed_ips(user_id: int):
        async with async_session() as db_session:
            from app.api.v1.allowed_ips.repository import IPRepository

            allowed_ips = await IPRepository().get_allowed_ips(db_session, user_id)
            return [ip.ip for ip in allowed_ips]

    @staticmethod
    async def get_role_permissions(role):
        async with async_session() as db_session:
            from app.api.v1.role_permissions.repository import RolePermissionRepository

            role_permissions = (
                await RolePermissionRepository().get_role_permissions_by_role_slug(
                    db_session, role
                )
            )
            return role_permissions
