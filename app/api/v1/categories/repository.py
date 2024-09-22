from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from core.exception import NotFoundException, BadRequestException
from core.models import Category


class CategoryRepository:
    async def get(self, db_session: AsyncSession, category_id: int):
        category = await db_session.get(Category, category_id)
        if not category:
            raise NotFoundException(error={"data": "دسته بندی یافت نشد"})
        return category

    async def create(self, db_session: AsyncSession, **data):
        new_category = Category(**data)
        db_session.add(new_category)
        await db_session.commit()
        await db_session.refresh(new_category)
        return new_category

    async def update(self, db_session: AsyncSession, category_id: int, **data):
        category = await self.get(db_session, category_id)
        for key, value in data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        await db_session.commit()
        await db_session.refresh(category)
        return category

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

    async def delete(self, db_session: AsyncSession, category_id: int):
        category = await self.get(db_session, category_id)

        try:
            await db_session.delete(category)
            await db_session.commit()
        except sa.exc.IntegrityError:
            raise BadRequestException(
                error={"data": "کتابی با این دسته بندی وجود دارد و قابل حذف نمی‌باشد"}
            )

        return {"message": "دسته بندی با موفقیت حذف شد"}
