from fastapi import APIRouter
from .authentication import auth_router
from .books import book_router
from .book_images import image_router
from .authors import author_router
from .categories import category_router
from .loans import loan_router
from .allowed_ips import ip_router
from .roles import role_router
from .permissions import permission_router
from .users import user_router
from .role_permissions import role_permission_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(book_router)
v1_router.include_router(image_router)
v1_router.include_router(author_router)
v1_router.include_router(category_router)
v1_router.include_router(loan_router)
v1_router.include_router(ip_router)
v1_router.include_router(role_router)
v1_router.include_router(permission_router)
v1_router.include_router(user_router)
v1_router.include_router(role_permission_router)
