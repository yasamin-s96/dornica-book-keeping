from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.v1.allowed_ips.schema.request import AllowedIP
from core.models import AllowedIPs
from core.exception.base import (
    NotFoundException,
)


class IPRepository:

    async def store_allowed_ips(
        self, db_session: AsyncSession, user_id: int, allowed_ips: list[AllowedIP]
    ):
        for ip in allowed_ips:
            new_ip = AllowedIPs(user_id=user_id, ip=ip.ip_address)
            db_session.add(new_ip)

        await db_session.commit()
        return {"message": "آی پی های مجاز با موفقیت ذخیره شد"}

    async def get_allowed_ips(self, db_session: AsyncSession, user_id: int):
        allowed_ips = list(
            (await db_session.execute(sa.select(AllowedIPs).filter_by(user_id=user_id)))
            .scalars()
            .all()
        )

        if not allowed_ips:
            raise NotFoundException(error="آی پی های مجازی برای این کاربر یافت نشد")

        return allowed_ips

    async def store_allowed_ip(self, db_session: AsyncSession, user_id: int, ip: str):
        new_ip = AllowedIPs(user_id=user_id, ip=ip)
        db_session.add(new_ip)

        await db_session.commit()
        await db_session.refresh(new_ip)
        return new_ip
