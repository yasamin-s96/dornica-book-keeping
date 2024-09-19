from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from core.models import Author


class AuthorRepository:
    async def get(self, db_session: AsyncSession, author_id: int):
        pass

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
