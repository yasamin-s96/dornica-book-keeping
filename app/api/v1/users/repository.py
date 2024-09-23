from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from core.models import User, Role, Permission, RolePermission
from core.security.password_handler import hash
from core.exception.base import NotFoundException


class UserRepository:

    async def create(self, db_session: AsyncSession, **data):
        hashed_password = hash(data.get("password"))

        new_user = User(
            email=data.get("email"),
            role_id=data.get("role_id"),
            password=hashed_password,
            phone_number=data.get("phone_number"),
        )
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)

        return new_user.email

    async def admin_create(self, db_session: AsyncSession, **data):
        hashed_password = hash(data.get("password"))

        new_user = User(
            email=data.get("email"),
            role_id=data.get("role_id"),
            password=hashed_password,
            phone_number=data.get("phone_number"),
        )
        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)

        return new_user

    async def email_exists(self, db_session: AsyncSession, email: str) -> bool:
        query = sa.select(sa.exists().where(User.email == email))
        result = bool((await db_session.execute(query)).scalars().one())
        return result

    async def user_exists(self, db_session: AsyncSession, user_id: int):
        result = bool(
            (await db_session.execute(sa.select(sa.exists().where(User.id == user_id))))
            .scalars()
            .first()
        )
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

    async def update_user_role(self, db_session: AsyncSession, user, new_role):
        user.role_id = new_role.id
        await db_session.commit()
        return user
