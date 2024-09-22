import datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class LoanRequest(BaseModel):
    loan_date: datetime.date
    return_date: datetime.date

    @field_validator("loan_date", "return_date", mode="before")
    @classmethod
    def iso_date(cls, value: str, info: FieldValidationInfo) -> datetime.date:
        assert isinstance(value, str), (
            info.field_name + "باید به صورت yyyy/mm/dd یا yyyy-mm-dd وارد شود"
        )
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass

        try:
            return datetime.datetime.strptime(value, "%Y/%m/%d").date()
        except ValueError:
            pass

        raise ValueError(
            f"{info.field_name}باید به صورت yyyy/mm/dd یا yyyy-mm-dd وارد شود "
        )


class ExtendLoanRequest(BaseModel):
    new_due_date: datetime.date

    @field_validator("new_due_date", mode="before")
    @classmethod
    def iso_date(cls, value: str, info: FieldValidationInfo) -> datetime.date:
        assert isinstance(value, str), (
            info.field_name + "باید به صورت yyyy/mm/dd یا yyyy-mm-dd وارد شود"
        )
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            pass

        try:
            return datetime.datetime.strptime(value, "%Y/%m/%d").date()
        except ValueError:
            pass

        raise ValueError(
            f"{info.field_name}باید به صورت yyyy/mm/dd یا yyyy-mm-dd وارد شود "
        )
