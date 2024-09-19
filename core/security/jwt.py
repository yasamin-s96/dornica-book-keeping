from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from starlette import status

from settings import settings


class JWTHandler:
    secret_key = settings.secret_key
    algorithm = settings.jwt_algorithm
    expire_in_days = settings.jwt_expire_time

    @staticmethod
    def encode(payload: dict) -> str:
        expire = datetime.utcnow() + timedelta(days=JWTHandler.expire_in_days)
        payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm]
            )
        except ExpiredSignatureError as exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Expired",
            )
        except JWTError as exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Not Found",
            )
