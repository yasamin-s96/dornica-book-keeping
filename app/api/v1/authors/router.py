from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi import APIRouter, Depends, Security

from app.api.v1.authors.controller import AuthorController
from app.api.v1.authors.schema.request import AuthorRequest, AuthorUpdateRequest
from app.api.v1.authors.schema.response import AuthorResponse
from core.connections.database_connection import create_session
from core.security.check_auth import AuthenticationRequired


author_router = APIRouter(prefix="/authors", tags=["Authors"])
author_controller = AuthorController()


@author_router.post(
    "/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED
)
async def create_author(
    author: AuthorRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await author_controller.add(
        db_session, **author.model_dump(exclude_unset=True)
    )


@author_router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author: AuthorUpdateRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await author_controller.update(
        db_session, author_id, **author.model_dump(exclude_unset=True)
    )


@author_router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await author_controller.delete(db_session, author_id)
