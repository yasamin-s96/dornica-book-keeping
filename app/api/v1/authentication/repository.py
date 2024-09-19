import datetime

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.v1.authentication.utilities import generate_verification_code
from core.connections.redis import whitelist, redis_db
from core.exception.custom import EmailNotVerifiedException
from core.models import User, Role
from core.security import JWTHandler
from core.security.password_handler import hash, verify
from core.enums import RoleSlug
from core.exception.base import (
    BadRequestException,
    AuthenticationFailedException,
    NotFoundException,
    ForbiddenException,
)
from settings import settings


class AuthRepository:
    async def register(self, db_session: AsyncSession, **data) -> User:
        email = data.get("email")
        phone = data.get("phone_number")
        raw_password = data.get("password")

        if await self.email_exists(db_session, email):
            raise BadRequestException(
                message="کاربر با ایمیل وارد شده از قبل وجود دارد"
            )

        # hashing password
        hashed_password = hash(raw_password)

        # getting related role
        user_role_id = (
            await db_session.execute(
                sa.select(Role.id).where(Role.slug == RoleSlug.USER)
            )
        ).scalar_one()

        new_user = User(
            email=email,
            role_id=user_role_id,
            password=hashed_password,
            phone_number=phone,
        )
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)

        return new_user.email

    async def verify_email(self, db_session: AsyncSession, verification_token: str):
        payload = JWTHandler.decode(verification_token)
        user_email = payload.get("email")
        user = await self.get_user(db_session, email=user_email)
        if user:
            user.is_verified = True
            await db_session.commit()
            return {"message": "تایید آدرس ایمیل با موفقیت انجام شد"}

        raise AuthenticationFailedException(message="توکن نامعتبر است")

    async def login(self, db_session: AsyncSession, **credentials):
        email = credentials.get("email")
        password = credentials.get("password")

        user = await self.get_user(db_session, email=email)
        if not user:
            raise AuthenticationFailedException(message="ایمیل یا کلمه عبور اشتباه است")

        is_password_valid = verify(
            hashed_password=user.password, plain_password=password
        )

        if not is_password_valid:
            raise AuthenticationFailedException(message="ایمیل یا کلمه عبور اشتباه است")

        if not user.is_verified:
            raise EmailNotVerifiedException()

        # generating verification code
        verification_code = generate_verification_code()
        redis_db.set(verification_code, user.id, ex=datetime.timedelta(minutes=2))
        print(verification_code)
        return {"message": "کد تایید، به شماره ای که با آن ثبت نام کرده اید ارسال شد"}

    async def email_exists(self, db_session: AsyncSession, email: str) -> bool:
        query = sa.select(sa.exists().where(User.email == email))
        result = bool((await db_session.execute(query)).scalars().one())
        return result

    async def get_user(
        self,
        db_session: AsyncSession,
        user_id: int | None = None,
        email: str | None = None,
    ):
        user = None

        if email:
            user = (
                await db_session.execute(sa.select(User).where(User.email == email))
            ).scalar_one_or_none()

        if user_id:
            user = (
                await db_session.execute(sa.select(User).where(User.id == user_id))
            ).scalar_one_or_none()

        if user is None:
            raise NotFoundException(message="کاربری بااین مشخصات یافت نشد")

        return user

    async def get_user_role(self, db_session: AsyncSession, user_role_id: int):
        user_role = (
            (
                await db_session.execute(
                    sa.select(Role.slug).where(Role.id == user_role_id)
                )
            )
            .scalars()
            .first()
        )
        return user_role

    async def change_password(self, db_session: AsyncSession, new_password: str):
        user_id = redis_db.get("reset_requested_by")

        if user_id is None:
            raise ForbiddenException

        try:
            user = await self.get_user(db_session, user_id=user_id)
        except NotFoundException:
            raise ForbiddenException

        redis_db.delete("reset_requested_by")

        new_password = hash(new_password)
        user.password = new_password
        await db_session.commit()
        return {"message": "کلمه عبور با موفقیت تغییر کرد"}
