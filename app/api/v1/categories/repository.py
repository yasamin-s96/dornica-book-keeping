from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from core.models import Category


class CategoryRepository:
    async def get(self, db_session: AsyncSession, category_id: int):
        pass

    async def exists(self, db_session: AsyncSession, category_id: int) -> bool:
        result = bool(
            (
                await db_session.execute(
                    sa.select(sa.exists().where(Category.id == category_id))
                )
            )
            .scalars()
            .one()
        )

        return result
