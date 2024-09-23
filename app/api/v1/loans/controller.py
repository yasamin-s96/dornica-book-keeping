from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.exception import BadRequestException, NotFoundException
from .repository import LoanRepository
from ..books.repository import BookRepository
from ..users.repository import UserRepository


class LoanController:
    def __init__(self):
        self.main_repo = LoanRepository()
        self.book_repo = BookRepository()
        self.user_repo = UserRepository()

    async def borrow(
        self, db_session: AsyncSession, user_id: int, book_id: int, **time_data
    ):
        errors = []
        try:
            book = await self.book_repo.get(db_session, book_id)
        except NotFoundException:
            errors.append({"book_id": "کتاب با این شناسه وجود ندارد"})

        if not await self.user_repo.user_exists(db_session, user_id):
            errors.append({"user_id": "کاربر با این شناسه وجود ندارد"})

        # raised exception if either book or user is not found
        if errors:
            raise BadRequestException(error=errors)

        if book.stock == 0 or book.is_active is False:
            raise BadRequestException(error={"stock": "کتاب موجود نیست"})

        result = await self.main_repo.borrow(db_session, user_id, book_id, **time_data)
        await self.book_repo.update_stock(
            db_session, quantity=1, book_id=book.id, operator="-"
        )
        return result

    async def return_book(self, db_session: AsyncSession, loan_id: int):
        updated_loan = await self.main_repo.return_book(db_session, loan_id)
        await self.book_repo.update_stock(
            db_session, quantity=1, book_id=updated_loan.book_id, operator="+"
        )
        return {"message": "کتاب با موفقیت پس گرفته شد"}

    async def extend(
        self, db_session: AsyncSession, loan_id: int, new_due_date: datetime.date
    ):
        return await self.main_repo.extend(db_session, loan_id, new_due_date)

    async def get_loans_report(
        self, db_session: AsyncSession, skip: int, limit: int, **filters
    ):
        return await self.main_repo.get_loans_report(
            db_session, skip=skip, limit=limit, **filters
        )
