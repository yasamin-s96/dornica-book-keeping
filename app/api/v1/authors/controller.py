from sqlalchemy.ext.asyncio import AsyncSession
from .repository import AuthorRepository


class AuthorController:
    def __init__(self):
        self.repo = AuthorRepository()

    async def add(self, db_session: AsyncSession, **data):
        return await self.repo.add(db_session, **data)

    async def update(self, db_session: AsyncSession, author_id: int, **data):
        return await self.repo.update(db_session, author_id, **data)

    async def delete(self, db_session: AsyncSession, author_id: int):
        return await self.repo.delete(db_session, author_id)
