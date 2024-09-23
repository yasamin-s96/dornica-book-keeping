from core.models import User, Loan, Category
from .validators import iso_date


def clean_filters(**filters):
    return {k: v for k, v in filters.items() if v is not None and v != ""}


def construct_loan_filters_list(**filters) -> list:
    filter_list = []
    if "loan_date_from" in filters:
        loan_date_from = iso_date(filters["loan_date_from"])
    if "loan_date_to" in filters:
        loan_date_to = iso_date(filters["loan_date_to"])

    if "return_date_from" in filters:
        return_date_from = iso_date(filters["return_date_from"])
    if "return_date_to" in filters:
        return_date_to = iso_date(filters["return_date_to"])

    if "loan_date_from" in filters and "loan_date_to" not in filters:
        filter_list.append(Loan.loan_date >= loan_date_from)

    if "loan_date_to" in filters and "loan_date_from" not in filters:
        filter_list.append(Loan.loan_date <= loan_date_to)

    if "loan_date_from" in filters and "loan_date_to" in filters:
        filter_list.append(Loan.loan_date.between(loan_date_from, loan_date_to))

    if "return_date_from" in filters and "return_date_to" not in filters:
        filter_list.append(Loan.return_date >= return_date_from)
    if "return_date_to" in filters and "return_date_from" not in filters:
        filter_list.append(Loan.return_date <= return_date_to)

    if "return_date_from" in filters and "return_date_to" in filters:
        filter_list.append(Loan.return_date.between(return_date_from, return_date_to))
    if "user" in filters:
        filter_list.append(User.email.ilike(f"%{filters['user']}%"))

    if "category" in filters:
        filter_list.append(Category.title.ilike(f"%{filters['category']}%"))

    return filter_list
