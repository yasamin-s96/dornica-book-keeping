from sqlalchemy.ext.asyncio import AsyncSession

from core.exception import BadRequestException
from .repository import CategoryRepository


class CategoryController:
    def __init__(self):
        self.repo = CategoryRepository()

    async def create(self, db_session: AsyncSession, **data):
        if "parent_id" in data and not await self.repo.exists(
            db_session, data["parent_id"]
        ):
            raise BadRequestException(error={"data": "دسته بندی والد یافت نشد"})

        return await self.repo.create(db_session, **data)

    async def update(self, db_session: AsyncSession, category_id: int, **data):
        if "parent_id" in data and not await self.repo.exists(
            db_session, data["parent_id"]
        ):
            raise BadRequestException(error={"data": "دسته بندی والد یافت نشد"})

        return await self.repo.update(db_session, category_id, **data)

    async def delete(self, db_session: AsyncSession, category_id: int):
        return await self.repo.delete(db_session, category_id)
