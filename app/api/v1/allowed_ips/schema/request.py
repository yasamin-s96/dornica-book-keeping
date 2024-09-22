import re

from pydantic import BaseModel, field_validator, Field
from pydantic_core import PydanticCustomError
import ipaddress


class EmailRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        result = re.fullmatch(pattern, value)
        if result is None:
            raise ValueError("ایمیل وارد شده اشتباه است.")

        return value


class PasswordRequest(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        error = {}

        if len(value) < 8:
            error["length"] = "کلمه عبور باید حداقل 8 کاراکتر باشد."

        if not any(char.islower() for char in value):
            error["lowercase_char"] = "کلمه عبور باید حداقل یک حرف کوچک داشته باشد."

        if not any(char.isupper() for char in value):
            error["uppercase_char"] = "کلمه عبور باید حداقل یک حرف بزرگ داشته باشد."

        if not any(char.isdigit() for char in value):
            error["digit"] = "کلمه عبور باید حداقل یک عدد داشته باشد."

        if not any(char in "@$!%*?&" for char in value):
            error["symbol"] = (
                "کلمه عبور باید حداقل یک کاراکتر خاص داشته باشد (@$!%*?&)."
            )

        if error:
            context = {"error": error}
            raise PydanticCustomError(
                "value_error",
                "Invalid password.",
                context,
            )

        return value


class LoginCredentials(EmailRequest, PasswordRequest):
    pass


class RegistrationCredentials(EmailRequest, PasswordRequest):
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        if len(value) != 11 or not value.startswith("09"):
            raise ValueError("شماره تلفن همراه وارد شده اشتباه است.")
        return value


class PhoneNumberVerificationRequest(BaseModel):
    code: str


class AllowedIP(BaseModel):
    ip_address: str

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, value: str):
        try:
            return ipaddress.IPv4Address(value)
        except ipaddress.AddressValueError:
            raise ValueError("آدرس IP وارد شده اشتباه است")
