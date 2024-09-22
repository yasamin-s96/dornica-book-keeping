from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa
from core.exception import NotFoundException
from core.models import Loan


class LoanRepository:
    async def get(self, db_session: AsyncSession, loan_id: int):
        loan = await db_session.get(Loan, loan_id)
        if loan is None:
            raise NotFoundException(error={"data": "امانتی با این شناسه یافت نشد"})

        return loan

    async def get_by_user_id(self, db_session: AsyncSession, user_id: int):
        loans = list(
            (await db_session.execute(sa.select(Loan).filter_by(user_id=user_id)))
            .scalars()
            .all()
        )
        return loans

    async def borrow(
        self, db_session: AsyncSession, user_id: int, book_id: int, **data
    ):
        loan = Loan(user_id=user_id, book_id=book_id, **data)
        db_session.add(loan)
        await db_session.commit()
        return loan

    async def extend(
        self, db_session: AsyncSession, loan_id: int, new_due_date: datetime.date
    ):
        loan = await self.get(db_session, loan_id)
        loan.return_date = new_due_date
        loan.extended = True
        await db_session.commit()
        await db_session.refresh(loan)
        return loan

    async def return_book(self, db_session: AsyncSession, loan_id: int):
        loan = await self.get(db_session, loan_id)
        loan.is_returned = True
        await db_session.commit()
        await db_session.refresh(loan)
        return loan
