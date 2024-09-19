from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.book_images.repository import ImageRepository
from core.security.check_auth import AuthenticationRequired
from core.connections.database_connection import create_session

image_router = APIRouter(prefix="/images", tags=["Images"])
image_repository = ImageRepository()


@image_router.post("/upload")
async def upload_images(
    images: list[UploadFile],
    user: Annotated[dict, Depends(AuthenticationRequired.check_auth)],
    db: Annotated[AsyncSession, Depends(create_session)],
):
    return await image_repository.bulk_create(db, images)
