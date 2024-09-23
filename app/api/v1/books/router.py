from typing import Annotated
from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import AuthenticationRequired

from .controller import BookController
from .schema.request import AddBookRequest, UpdateBookRequest
from .schema.response import BookResponse, BookRawResponse
from core.connections.database_connection import create_session
from .utilities import clean_filters

book_router = APIRouter(prefix="/books", tags=["Books"])

book_controller = BookController()


@book_router.get("/", response_model=list[BookResponse])
async def get_books(
    db_session: Annotated[AsyncSession, Depends(create_session)],
    search: str | None = None,
    with_picture: bool | None = None,
    available: bool | None = None,
    category: str | None = None,
    author: str | None = None,
    author_nationality: str | None = None,
    pub_year: int | None = None,
    skip: int = 0,
    limit: int = 10,
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager", "user"]
    ),
):
    filters = clean_filters(
        search=search,
        with_picture=with_picture,
        available=available,
        category=category,
        author=author,
        author_nationality=author_nationality,
        pub_year=pub_year,
    )
    return await book_controller.list(db_session, skip=skip, limit=limit, **filters)


@book_router.post(
    "/", response_model=BookRawResponse, status_code=status.HTTP_201_CREATED
)
async def add_book(
    book: AddBookRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await book_controller.add(db_session, **book.model_dump(exclude_unset=True))


@book_router.put("/{book_id}", response_model=BookRawResponse)
async def update_book(
    book_id: int,
    book: UpdateBookRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await book_controller.update(
        db_session, book_id, **book.model_dump(exclude_unset=True)
    )


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await book_controller.delete(db_session, book_id)


@book_router.get("/inventory")
async def get_inventory(
    db_session: Annotated[AsyncSession, Depends(create_session)],
    category: str | None = None,
    # authorization=Security(
    #     AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    # ),
):
    return await book_controller.book_inventory_report(
        db_session, category_filter=category
    )
