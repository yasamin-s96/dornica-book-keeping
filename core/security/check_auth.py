from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Tuple, Annotated
from core.security import JWTHandler
from core.connections.redis import whitelist


class AuthenticationRequired:
    @staticmethod
    async def check_auth(
        req: Request,
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))
        ],
    ):
        if not credentials:
            raise HTTPException(status_code=401, detail="Access Required")
        token = credentials.credentials
        payload = JWTHandler.decode(token)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid Token")

        client_ip = req.client.host
        token_ip = payload.get("ip")
        ip_check = payload.get("ip_check")
        if client_ip != token_ip:
            raise HTTPException(status_code=401, detail="IP Not Allowed")

        # exist in whitelist
        if not whitelist.get(token):
            raise HTTPException(status_code=401, detail="Authentication Required")

        # if ip_check == 1:
        #     from app.api.v1.user_ip.repository import UserIpRepository
        #
        #     user_allowed_ips = UserIpRepository.get_user_ips(payload.get("user_id"))
        #     if client_ip not in user_allowed_ips:
        #         raise HTTPException(status_code=401, detail="IP Not Allowed")

        return payload
