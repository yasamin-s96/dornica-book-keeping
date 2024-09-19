from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Body
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .controller import AuthController
from core.connections.database_connection import create_session
from core.email import send_email_verification_link
from .schema.request import (
    RegistrationCredentials,
    LoginCredentials,
    EmailRequest,
    PasswordRequest,
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

auth = AuthController()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    credentials: RegistrationCredentials,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    background_tasks: BackgroundTasks,
):
    user_email = await auth.register(db_session, **credentials.model_dump())
    background_tasks.add_task(send_email_verification_link, user_email)
    return {"message": "کاربر با موفقیت ثبت شد. لینک تایید به ایمیل شما ارسال می شود."}


@auth_router.post("/login")
async def login(
    credentials: LoginCredentials,
    db_session: Annotated[AsyncSession, Depends(create_session)],
):
    return await auth.login(db_session, **credentials.model_dump())


@auth_router.get("/verify-email")
async def verify_email(
    token: str, db_session: Annotated[AsyncSession, Depends(create_session)]
):
    return await auth.verify_email(db_session, token)


@auth_router.post("/two-factor-auth", status_code=status.HTTP_200_OK)
async def two_factor_auth(
    request: Request,
    verification_code: Annotated[str, Body()],
    db_session: Annotated[AsyncSession, Depends(create_session)],
):
    return await auth.generate_auth_token(
        db_session, request.client.host, verification_code
    )


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def request_reset_password_link(
    email: EmailRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    background_tasks: BackgroundTasks,
):
    return await auth.request_reset_password(db_session, email.email, background_tasks)


@auth_router.post("/reset-link")
async def check_reset_token(
    token: str, db_session: Annotated[AsyncSession, Depends(create_session)]
):
    await auth.verify_reset_password_token(db_session, token)


@auth_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    new_password: PasswordRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
):
    return await auth.reset_password(db_session, new_password.password)
