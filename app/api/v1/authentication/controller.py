import datetime

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from core.connections.redis import redis_db, whitelist
from core.security.password_handler import verify
from .utilities import send_email_verification_link, send_reset_password_link
from core.exception import (
    AuthenticationFailedException,
    NotFoundException,
    BadRequestException,
    ForbiddenException,
)
from core.exception.custom import EmailNotVerifiedException
from core.security import JWTHandler
from settings import settings
from .repository import AuthRepository
from .utilities import generate_verification_code
from ..allowed_ips.repository import IPRepository
from ..allowed_ips.schema.request import AllowedIP
from ..permissions.repository import PermissionRepository
from ..role_permissions.repository import RolePermissionRepository
from ..roles.repository import RoleRepository
from ..users.repository import UserRepository


class AuthController:
    def __init__(self):
        self.main_repo = AuthRepository()
        self.user_repo = UserRepository()
        self.permission_repo = PermissionRepository()
        self.role_repo = RoleRepository()
        self.role_permissions_repo = RolePermissionRepository()
        self.ip_repo = IPRepository()

    async def register(self, db_session: AsyncSession, **credentials):
        email = credentials.get("email")
        if await self.user_repo.email_exists(db_session, email):
            raise BadRequestException(
                message="کاربر با ایمیل وارد شده از قبل وجود دارد"
            )
        role = await self.role_repo.get_role_by_slug(db_session, "user")
        credentials.update({"role_id": role.id})
        return await self.user_repo.create(db_session, **credentials)

    async def verify_email(self, db_session: AsyncSession, token: str):
        payload = JWTHandler.decode(token)
        user_email = payload.get("email")
        user = await self.user_repo.get_user(db_session, email=user_email)
        if user:
            return await self.main_repo.verify_email(db_session, user)
        raise AuthenticationFailedException(error="توکن نامعتبر است")

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

        user = await self.user_repo.get_user(db_session, user_id=user_id)

        role = await self.role_repo.get_role_by_id(db_session, user.role_id)

        role_permissions = (
            await self.role_permissions_repo.get_role_permissions_by_role_slug(
                db_session, role.slug
            )
        )

        payload = {
            "user_id": user.id,
            "ip": ip,
            "ip_check": user.ip_check,
            "scope": role.slug,
            "permissions": role_permissions,
        }

        token = JWTHandler.encode(payload)

        whitelist.set(
            token,
            user_id,
            ex=settings.whitelist_token_expire_time,
        )

        if user.ip_check is True:
            await self.ip_repo.store_allowed_ip(db_session, user.id, ip)

        await self.main_repo.record_login(db_session, user.id, ip)

        return {"token": token, "type": "Bearer"}

    async def login(self, db_session: AsyncSession, **credentials):
        email = credentials.get("email")
        password = credentials.get("password")

        user = await self.user_repo.get_user(db_session, email=email)
        if not user:
            raise AuthenticationFailedException(message="ایمیل یا کلمه عبور اشتباه است")

        is_password_valid = verify(
            hashed_password=user.password, plain_password=password
        )

        if not is_password_valid:
            raise AuthenticationFailedException(message="ایمیل یا کلمه عبور اشتباه است")

        if not user.is_verified:
            send_email_verification_link(credentials["email"])
            raise EmailNotVerifiedException()

        verification_code = generate_verification_code()
        redis_db.set(verification_code, user.id, ex=datetime.timedelta(minutes=2))
        print(verification_code)
        return {"message": "کد تایید، به شماره ای که با آن ثبت نام کرده اید ارسال شد"}

    async def request_reset_password(
        self, db_session: AsyncSession, email: str, background_tasks: BackgroundTasks
    ):
        user = await self.user_repo.get_user(db_session, email=email)
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
        user = await self.user_repo.get_user(db_session, email=user_email)

        if user:
            if user.is_active:
                redis_db.set(
                    verification_token, user.id, ex=datetime.timedelta(minutes=5)
                )
            else:
                raise AuthenticationFailedException("اکانت شما فعال نمی باشد")

    async def reset_password(
        self, db_session: AsyncSession, new_password: str, verified_token: str
    ):
        user_id = redis_db.get(verified_token)

        if user_id is None:
            raise ForbiddenException

        try:
            user = await self.user_repo.get_user(db_session, user_id=user_id)
            redis_db.delete(verified_token)
        except NotFoundException:
            raise ForbiddenException

        return await self.main_repo.change_password(db_session, new_password, user)

    async def logout(self, db_session: AsyncSession, token: str, user_id: int):
        await self.user_repo.get_user(db_session, user_id=user_id)
        await self.main_repo.record_logout(db_session, user_id)
        whitelist.delete(token)
        return {"message": "خروج با موفقیت انجام شد"}
