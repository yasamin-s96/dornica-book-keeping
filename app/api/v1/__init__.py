from fastapi import APIRouter
from .authentication import auth_router
from .books import book_router
from .book_images import image_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(book_router)
v1_router.include_router(image_router)
