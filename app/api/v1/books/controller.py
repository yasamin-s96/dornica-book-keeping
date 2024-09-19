from sqlalchemy.ext.asyncio import AsyncSession

from core.exception import NotFoundException, BadRequestException
from .repository import BookRepository
from ..authors.repository import AuthorRepository
from ..book_images.repository import ImageRepository
from ..categories.repository import CategoryRepository


class BookController:
    def __init__(self):
        self.main_repo = BookRepository()
        self.image_repo = ImageRepository()
        self.author_repo = AuthorRepository()
        self.category_repo = CategoryRepository()

    async def list(
        self, db_session: AsyncSession, skip: int = 0, limit: int = 10, **filters
    ):
        return await self.main_repo.list(db_session, skip, limit, **filters)

    async def add(self, db_session: AsyncSession, **data):
        errors = {}
        author_exists = await self.author_repo.exists(db_session, data["author_id"])
        category_exists = await self.category_repo.exists(
            db_session, data["category_id"]
        )
        if not author_exists:
            errors["author_id"] = "نویسنده ای با این مقدار وجود ندارد"

        if not category_exists:
            errors["category_id"] = "دسته بندی با این مقدار وجود ندارد"

        if errors:
            raise BadRequestException(error=errors)

        image_ids = data.pop("image_ids", None)
        new_book = await self.main_repo.create(db_session, **data)

        if image_ids:
            for image_id in image_ids:
                await self.image_repo.update(
                    db_session, image_id, book_id=new_book.id, in_use=True
                )
        return new_book

    async def update(self, db_session: AsyncSession, book_id: int, **data):
        errors = {}
        if "author_id" in data:
            author_exists = await self.author_repo.exists(db_session, data["author_id"])
            if not author_exists:
                errors["author_id"] = "نویسنده ای با این مقدار وجود ندارد"

        if "category_id" in data:
            category_exists = await self.category_repo.exists(
                db_session, data["category_id"]
            )
            if not category_exists:
                errors["category_id"] = "دسته بندی با این مقدار وجود ندارد"

        if errors:
            raise BadRequestException(error=errors)

        new_image_ids = data.pop("image_ids", None)
        modified_book = await self.main_repo.update(db_session, book_id, **data)
        if new_image_ids:
            current_book_images = await self.image_repo.get_by_book_id(
                db_session, modified_book.id
            )
            if current_book_images:
                for image in current_book_images:
                    if image.id not in new_image_ids:
                        await self.image_repo.update_by_book_id(
                            db_session, modified_book.id, book_id=None, in_use=False
                        )

            for image_id in new_image_ids:
                await self.image_repo.update(
                    db_session, image_id, book_id=modified_book.id, in_use=True
                )
        return modified_book

    async def delete(self, db_session: AsyncSession, book_id: int):
        return await self.main_repo.delete(db_session, book_id)
