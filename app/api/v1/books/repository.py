import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
from .schema.response import BookResponse
from core.models import Book, Author, Category, Image
from core.exception import NotFoundException, BadRequestException
from .utilities import construct_filters_list


class BookRepository:

    async def create(self, db_session: AsyncSession, **data):
        new_book = Book(**data)
        db_session.add(new_book)
        await db_session.commit()
        await db_session.refresh(new_book)

        return new_book

    async def list(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 10, **filters
    ):
        base_image_url = f"http://{settings.image_host}:{settings.image_port}/"
        query = (
            sa.select(
                Book.id,
                Book.title,
                Author.name.label("author"),
                Category.title.label("category"),
                Book.stock,
                Book.publication_year,
                sa.func.group_concat(Image.path).label("image_urls"),
            )
            .outerjoin(Image, Book.id == Image.book_id)
            .join(Author, Book.author_id == Author.id)
            .join(Category, Book.category_id == Category.id)
            .group_by(Book.id, Author.id, Category.id)
        )

        if filters:
            flist = construct_filters_list(**filters)
            query = query.where(sa.and_(*flist))

        query = query.offset(skip).limit(limit)

        result = (await db_session.execute(query)).all()

        books = []
        for row in result:
            image_urls = (
                [base_image_url + url.strip() for url in row.image_urls.split(",")]
                if row.image_urls
                else []
            )

            book = BookResponse(
                id=row.id,
                title=row.title,
                author=row.author,
                category=row.category,
                stock=row.stock,
                publication_year=row.publication_year,
                image_urls=image_urls,
            )
            books.append(book)

        return books

    async def get(self, db_session: AsyncSession, book_id: int):
        book = await db_session.get(Book, book_id)
        if not book:
            raise NotFoundException(error={"data": "کتاب یافت نشد"})

        return book

    async def update(self, db_session: AsyncSession, book_id: int, **data):
        book = await self.get(db_session, book_id)
        for key, value in data.items():
            if hasattr(book, key):
                setattr(book, key, value)

        await db_session.commit()
        await db_session.refresh(book)

        return book

    async def update_stock(
        self, db_session: AsyncSession, book_id: int, quantity: int, operator: str = "+"
    ):
        if operator not in ["+", "-"]:
            raise BadRequestException(error={"data": "عملگر آپدیت معتبر نیست"})

        book = await self.get(db_session, book_id)
        if operator == "+":
            book.stock += quantity
        else:
            book.stock -= quantity
        await db_session.commit()

    async def delete(self, db_session: AsyncSession, book_id: int):
        try:
            query = sa.delete(Book).where(Book.id == book_id)
            row = (await db_session.execute(query)).rowcount
        except sa.exc.IntegrityError:
            raise BadRequestException(
                error={"data": "کتاب در دیگر رکورد ها دارای وابستگی است"}
            )

        if row == 0:
            raise NotFoundException(error={"data": "کتاب یافت نشد"})
        await db_session.commit()
        return {"message": "کتاب با موفقیت حذف شد"}
