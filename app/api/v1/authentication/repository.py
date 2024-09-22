import datetime

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from core.models import LoginHistory
from core.security.password_handler import hash
from core.exception.base import NotFoundException


class AuthRepository:

    async def verify_email(self, db_session: AsyncSession, user):
        user.is_verified = True
        await db_session.commit()
        return {"message": "تایید آدرس ایمیل با موفقیت انجام شد"}

    async def change_password(self, db_session: AsyncSession, new_password: str, user):
        new_password = hash(new_password)
        user.password = new_password
        await db_session.commit()
        return {"message": "کلمه عبور با موفقیت تغییر کرد"}

    async def record_login(
        self, db_session: AsyncSession, user_id: int, ip_address: str
    ):
        login_history = LoginHistory(user_id=user_id, ip_address=ip_address)
        db_session.add(login_history)
        await db_session.commit()

    async def record_logout(self, db_session: AsyncSession, user_id: int):
        latest_login_by_user = (
            await db_session.execute(
                sa.select(LoginHistory)
                .filter_by(user_id=user_id)
                .order_by(LoginHistory.login_time.desc())
            )
        ).scalar_one_or_none()

        if not latest_login_by_user:
            raise NotFoundException("رکوردهای ورود برای این کاربر یافت نشد")

        else:
            latest_login_by_user.logout_time = datetime.datetime.now()
            await db_session.commit()
