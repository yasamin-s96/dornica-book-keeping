from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from app.api.v1.loans.utilities import clean_filters, construct_loan_filters_list
from core.exception import NotFoundException
from core.models import Loan, User, Book, Category


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

    async def get_loans_report(
        self,
        db_session: AsyncSession,
        skip: int = 0,
        limit: int = 0,
        **filters,
    ):
        query = (
            sa.select(
                Loan.id,
                User.email,
                Book.title,
                Category.title.label("category"),
                Loan.is_returned,
                Loan.extended,
                Loan.loan_date,
                Loan.return_date,
            )
            .select_from(Loan)
            .join(User, User.id == Loan.user_id)
            .join(Book, Book.id == Loan.book_id)
            .join(Category, Category.id == Book.category_id)
        )

        if filters:
            cleaned_filters = clean_filters(**filters)
            listed_filters = construct_loan_filters_list(**cleaned_filters)
            query = query.filter(sa.and_(*listed_filters))

        query = query.order_by(Loan.return_date.desc()).limit(limit).offset(skip)

        loans_report = await db_session.execute(query)

        return [
            {
                "id": row.id,
                "user": row.email,
                "book": row.title,
                "category": row.category,
                "is_returned": row.is_returned,
                "extended": row.extended,
                "loan_date": row.loan_date,
                "retun_date": row.return_date,
            }
            for row in loans_report
        ]
