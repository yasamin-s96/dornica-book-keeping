from typing import Callable

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from settings import settings


engine = create_async_engine(url=str(settings.mysql_dsn), echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


def manage_db_session(func: Callable):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, session=session, **kwargs)

    return wrapper


async def create_session():
    async with async_session() as session:
        yield session


class Base(DeclarativeBase): ...
