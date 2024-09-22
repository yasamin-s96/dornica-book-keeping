from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from core.exception import NotFoundException, BadRequestException
from core.models import Author


class AuthorRepository:

    async def add(self, db_session: AsyncSession, **data) -> Author:
        author = Author(**data)
        db_session.add(author)
        await db_session.commit()
        return author

    async def get(self, db_session: AsyncSession, author_id: int):
        author = await db_session.get(Author, author_id)
        if not author:
            raise NotFoundException(error={"data": "نویسنده یافت نشد"})
        return author

    async def update(self, db_session: AsyncSession, author_id: int, **data):
        author = await self.get(db_session, author_id)
        for key, value in data.items():
            if hasattr(author, key):
                setattr(author, key, value)
        await db_session.commit()
        await db_session.refresh(author)
        return author

    async def delete(self, db_session: AsyncSession, author_id: int):
        author = await self.get(db_session, author_id)
        try:
            await db_session.delete(author)
            await db_session.commit()
        except sa.exc.IntegrityError:
            raise BadRequestException(
                error={"data": "کتاب با این نویسنده وجود دارد و قابل حذف نمی‌باشد"}
            )
        return {"message": "نویسنده با موفقیت حذف شد"}

    async def exists(self, db_session: AsyncSession, author_id: int) -> bool:
        result = bool(
            (
                await db_session.execute(
                    sa.select(sa.exists().where(Author.id == author_id))
                )
            )
            .scalars()
            .one()
        )
        return result
