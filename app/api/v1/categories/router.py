from typing import Annotated

from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.v1.categories.controller import CategoryController
from app.api.v1.categories.schema.request import CategoryRequest, CategoryUpdateRequest
from app.api.v1.categories.schema.response import CategoryResponse
from core.connections.database_connection import create_session
from core.security import AuthenticationRequired

category_router = APIRouter(prefix="/categories", tags=["Categories"])
category_controller = CategoryController()


@category_router.post(
    "/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def add_category(
    category: CategoryRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await category_controller.create(
        db_session, **category.model_dump(exclude_unset=True)
    )


@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdateRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await category_controller.update(
        db_session, category_id, **category.model_dump(exclude_unset=True)
    )


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await category_controller.delete(db_session, category_id)
