from http import HTTPStatus
from fastapi import status
from pydantic import BaseModel
from typing import Generic, TypeVar, Callable


class CustomException(Exception):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = str
    error = any

    def __init__(self, message=None, error_code=None, error=None):
        if message:
            self.message = message
        if error_code:
            self.error_code = error_code
        if error:
            self.error = error


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = "خطایی در درخواست رخ داده است"
    error = HTTPStatus.BAD_REQUEST.description


class ConnectionException(CustomException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = 7005
    message = "خطا در اتصال به پایگاه داده"
    error = {"connection": ["خطا در ارتباط به پایگاه داده"]}


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = "دیتا یافت نشد"
    error = {"data": ["دیتا یافت نشد"]}


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = "کاربر دسترسی ندارد"
    error = {"access": ["کاربر دسترسی ندارد"]}


class UnauthorizedException(CustomException):
    code = status.HTTP_403_FORBIDDEN
    error_code = status.HTTP_403_FORBIDDEN
    message = "خطا در احراز هویت"
    error = {"access": ["خطا در احراز هویت"]}


class UnprocessableEntity(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = "خطا در اعتبار سنجی"
    error = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(CustomException):
    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = "Duplicate data"
    error = HTTPStatus.UNPROCESSABLE_ENTITY.description


class AuthenticationRequiredException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED
    message = "نیازمند احراز هویت"
    error = {"access": ["نیازمند احراز هویت"]}


class AuthenticationFailedException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED
    message = "خطا در احراز هویت"
    error = {"access": ["خطا در احراز هویت"]}


class TooManyRequestException(CustomException):
    code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = status.HTTP_429_TOO_MANY_REQUESTS
    message = "تعداد درخواست بیش از حد مجاز است. لطفا مجددا تلاش کنید"
    error = {"access": ["تعداد درخواست بیش از حد مجاز است. لطفا مجددا تلاش کنید"]}


class LogicException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = status.HTTP_400_BAD_REQUEST
    message = "خطا در منطق"
    error = HTTPStatus.BAD_REQUEST.description


class NotActiveException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = status.HTTP_400_BAD_REQUEST
    message = "اطلاعات در دسترس نیست"
    error = {"access": ["اطلاعات در دسترس نیست"]}


class ArchiveException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = status.HTTP_400_BAD_REQUEST
    message = "اطلاعات آرشیو شده است"
    error = {"access": ["اطلاعات آرشیو شده است"]}


class SystemRequestException(CustomException):
    code = status.HTTP_502_BAD_GATEWAY
    error_code = 750
    message = "خطا در سرویس دهنده"
    error = {"system": ["خطا در سرویس دهنده"]}


class ValidateFileException(CustomException):
    code = status.HTTP_400_BAD_REQUEST
    error_code = status.HTTP_400_BAD_REQUEST
    message = "فایل ورودی اشتباه است."
    error = HTTPStatus.BAD_REQUEST.description


class ServiceException(CustomException):
    internal_code: int = 200
    code = status.HTTP_400_BAD_REQUEST
    error_code = status.HTTP_400_BAD_REQUEST
    message = "خطا در منطق سرویس."
    error = HTTPStatus.BAD_REQUEST.description

    def __init__(self, internal_code: int, message=None, error_code=None, error=None):
        if internal_code is not None:
            self.internal_code = internal_code
        super().__init__(message=message)


class BaseDataNotFoundServiceException(ServiceException):
    internal_code: int = 202
    code = status.HTTP_400_BAD_REQUEST
    error_code = status.HTTP_400_BAD_REQUEST
    message = "اطلاعات پایه یافت نشد."
    error = HTTPStatus.BAD_REQUEST.description

    def __init__(
        self, internal_code: int = None, message=None, error_code=None, error=None
    ):
        super().__init__(internal_code=self.internal_code, message=message)
