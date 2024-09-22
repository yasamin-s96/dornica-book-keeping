from datetime import datetime, date

from pydantic import BaseModel


class LoanResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    loan_date: date
    return_date: date
    extended: bool = False
    is_returned: bool = False

    def to_str_date(self, value: date) -> str:
        return value.strftime("%Y-%m-%d")

    class Config:
        orm_mode = True
        json_encoders = {date: lambda v: v.strftime("%Y-%m-%d")}
