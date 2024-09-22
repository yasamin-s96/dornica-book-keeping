from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.book_images.repository import ImageRepository
from core.security.check_auth import AuthenticationRequired
from core.connections.database_connection import create_session

image_router = APIRouter(prefix="/images", tags=["Images"])
image_repository = ImageRepository()


@image_router.post("/upload")
async def upload_images(
    images: list[UploadFile],
    db: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await image_repository.bulk_create(db, images)
