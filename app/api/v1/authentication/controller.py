import datetime

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from core.connections.redis import redis_db, whitelist
from core.email import send_email_verification_link, send_reset_password_link
from core.exception import AuthenticationFailedException, NotFoundException
from core.exception.custom import EmailNotVerifiedException
from core.security import JWTHandler
from settings import settings
from .repository import AuthRepository


class AuthController:
    def __init__(self):
        self.repo = AuthRepository()

    async def register(self, db_session: AsyncSession, **credentials):
        return await self.repo.register(db_session, **credentials)

    async def verify_email(self, db_session: AsyncSession, token: str):
        return await self.repo.verify_email(db_session, token)

    async def verify_verification_code(self, user_entered_code):
        user_id = redis_db.get(user_entered_code)
        if user_id:
            return user_id
        else:
            raise AuthenticationFailedException(
                "کد تایید وارد شده اشتباه یا منقضی شده است"
            )

    async def generate_auth_token(
        self, db_session: AsyncSession, ip: str, user_entered_code: str
    ):
        user_id = await self.verify_verification_code(user_entered_code)

        user = await self.repo.get_user(db_session, user_id=user_id)

        user_role = await self.repo.get_user_role(db_session, user.role_id)

        payload = {
            "user_id": user.id,
            "ip": ip,
            "ip_check": user.ip_check,
            "scope": user_role,
        }

        token = JWTHandler.encode(payload)

        whitelist.set(
            name=token,
            value=user.id,
            ex=settings.whitelist_token_expire_time,
        )

        return {"token": token, "type": "Bearer"}

    async def login(self, db_session: AsyncSession, **credentials):
        try:
            return await self.repo.login(db_session, **credentials)

        except EmailNotVerifiedException:
            send_email_verification_link(credentials["email"])
            raise

    async def request_reset_password(
        self, db_session: AsyncSession, email: str, background_tasks: BackgroundTasks
    ):
        user = await self.repo.get_user(db_session, email=email)
        if not user.is_verified:
            send_email_verification_link(email)
            raise EmailNotVerifiedException()

        else:
            background_tasks.add_task(send_reset_password_link, email)
            return {"message": "لینک بازیابی کلمه عبور به ایمیل شما ارسال شد"}

    async def verify_reset_password_token(
        self, db_session: AsyncSession, verification_token: str
    ):
        payload = JWTHandler.decode(verification_token)
        user_email = payload.get("forgot_password_email")
        user = await self.repo.get_user(db_session, email=user_email)

        if user:
            if user.is_active:
                redis_db.set(
                    "reset_requested_by", user.id, ex=datetime.timedelta(minutes=5)
                )
            else:
                raise AuthenticationFailedException("اکانت شما فعال نمی باشد")

    async def reset_password(self, db_session: AsyncSession, new_password: str):
        return await self.repo.change_password(db_session, new_password)
