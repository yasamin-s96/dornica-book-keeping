from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks, Body
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import AuthenticationRequired
from core.security.throttler import rate_limit
from .controller import AuthController
from core.connections.database_connection import create_session
from .utilities import send_email_verification_link
from .schema.request import (
    RegistrationCredentials,
    LoginCredentials,
    EmailRequest,
    PasswordRequest,
    PhoneNumberVerificationRequest,
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

auth = AuthController()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
@rate_limit(max_calls=5, time_frame=60)
async def register(
    credentials: RegistrationCredentials,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    background_tasks: BackgroundTasks,
):
    user_email = await auth.register(db_session, **credentials.model_dump())
    background_tasks.add_task(send_email_verification_link, user_email)
    return {"message": "کاربر با موفقیت ثبت شد. لینک تایید به ایمیل شما ارسال می شود."}


@auth_router.post("/login")
@rate_limit(max_calls=5, time_frame=60)
async def login(
    credentials: LoginCredentials,
    db_session: Annotated[AsyncSession, Depends(create_session)],
):
    return await auth.login(db_session, **credentials.model_dump())


@auth_router.put("/logout")
@rate_limit(max_calls=5, time_frame=60)
async def logout(
    db_session: Annotated[AsyncSession, Depends(create_session)],
    token: Annotated[
        HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))
    ],
    credentials=Depends(AuthenticationRequired.check_auth),
):

    user_id = credentials.get("user_id")
    return await auth.logout(db_session, token.credentials, user_id)


@auth_router.get("/verify-email")
@rate_limit(max_calls=5, time_frame=60)
async def verify_email(
    token: str, db_session: Annotated[AsyncSession, Depends(create_session)]
):
    return await auth.verify_email(db_session, token)


@auth_router.post("/two-factor-auth", status_code=status.HTTP_200_OK)
@rate_limit(max_calls=5, time_frame=60)
async def two_factor_auth(
    request: Request,
    verification_code: PhoneNumberVerificationRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
):
    return await auth.generate_auth_token(
        db_session, request.client.host, verification_code.code
    )


@auth_router.post("/forgot-password", status_code=status.HTTP_200_OK)
@rate_limit(max_calls=5, time_frame=60)
async def request_reset_password_link(
    email: EmailRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
    background_tasks: BackgroundTasks,
):
    return await auth.request_reset_password(db_session, email.email, background_tasks)


@auth_router.get("/verify-reset-link")
@rate_limit(max_calls=5, time_frame=60)
async def verify_reset_token(
    token: str, db_session: Annotated[AsyncSession, Depends(create_session)]
):
    await auth.verify_reset_password_token(db_session, token)


@auth_router.put("/reset-password", status_code=status.HTTP_200_OK)
@rate_limit(max_calls=5, time_frame=60)
async def reset_password(
    token: str,
    new_password: PasswordRequest,
    db_session: Annotated[AsyncSession, Depends(create_session)],
):
    return await auth.reset_password(db_session, new_password.password, token)
