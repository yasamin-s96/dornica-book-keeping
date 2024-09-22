from typing import Annotated

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security.check_auth import AuthenticationRequired
from .schema.request import *
from .schema.response import LoanResponse
from app.api.v1.loans.controller import LoanController
from core.connections.database_connection import create_session

loan_router = APIRouter(prefix="/book-loans", tags=["Loans"])
loan_controller = LoanController()


@loan_router.post(
    "/borrow/{book_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
)
async def borrow(
    book_id: int,
    user_request: LoanRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager", "user"]
    ),
    user_id=Depends(AuthenticationRequired.get_current_user_id),
):
    return await loan_controller.borrow(
        db_session, user_id, book_id, **user_request.model_dump()
    )


@loan_router.put(
    "/{loan_id}/extend", response_model=LoanResponse, status_code=status.HTTP_200_OK
)
async def extend_loan(
    loan_id: int,
    request: ExtendLoanRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await loan_controller.extend(db_session, loan_id, **request.model_dump())


@loan_router.put("/{loan_id}/return", status_code=status.HTTP_200_OK)
async def return_book(
    loan_id: int,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    authorization=Security(
        AuthenticationRequired.check_auth, scopes=["admin", "manager"]
    ),
):
    return await loan_controller.return_book(db_session, loan_id)
