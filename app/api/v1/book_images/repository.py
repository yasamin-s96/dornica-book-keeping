import sqlalchemy as sa
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from .file_handler import *
from core.exception import NotFoundException, ForbiddenException, BadRequestException
from core.models import Image


class ImageRepository:

    async def bulk_create(
        self,
        db_session: AsyncSession,
        files: list[UploadFile],
    ):
        images = []
        for file in files:
            check_file(file)
            path = construct_path_to_store_files(
                file.filename, directories=["book_images"]
            )
            with open(path, "wb") as f:
                file_bytes = await file.read(file.size)
                f.write(file_bytes)
                await file.close()

            new_image = Image(
                path=path,
                filename=file.filename,
                size=file.size,
                format=get_file_extension(file.filename),
            )
            images.append(new_image)

        db_session.add_all(images)
        await db_session.commit()

        image_ids = []
        for image in images:
            await db_session.refresh(image)
            image_ids.append(image.id)

        # Returning file image_ids
        return {"images": image_ids}

    async def get(self, db_session: AsyncSession, image_id: int):
        image = await db_session.get(Image, image_id)
        if not image:
            raise NotFoundException(error={"data": "عکس یافت نشد"})

        return image

    async def get_by_book_id(self, db_session: AsyncSession, book_id: int):
        images = (
            (await db_session.execute(sa.select(Image).where(Image.book_id == book_id)))
            .scalars()
            .all()
        )

        return images

    async def update(self, db_session: AsyncSession, image_id: int, **data):
        image = await self.get(db_session, image_id)

        for key, value in data.items():
            if hasattr(image, key):
                setattr(image, key, value)

        await db_session.commit()

    async def update_by_book_id(self, db_session: AsyncSession, book_id, **data):
        images = await self.get_by_book_id(db_session, book_id)

        if not images:
            raise NotFoundException(error={"data": "عکسی برای این کتاب یافت نشد"})

        for image in images:
            for key, value in data.items():
                if hasattr(image, key):
                    setattr(image, key, value)

        await db_session.commit()

    async def delete(self, db_session: AsyncSession, image_id: int):
        image = await self.get(db_session, image_id)

        if image.in_use is True:
            raise BadRequestException("عکس در حال استفاده است و نمی تواند حذف شود")

        await db_session.delete(image)
        await db_session.commit()

        return {"message": "عکس با موفقیت حذف شد"}
