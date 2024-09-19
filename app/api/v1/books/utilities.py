import sqlalchemy as sa
from core.models import Author, Book, Category, Image


def clean_filters(**filters):
    return {k: v for k, v in filters.items() if v is not None and v != ""}


def construct_filters_list(**filters) -> list:
    filter_list = []
    for key, value in filters.items():
        if key == "search":
            filter_list.append(Book.title.ilike(f"%{value}%"))
        if key == "with_picture" and value is True:
            filter_list.append(Image.book_id != None)
        if key == "available" and value is True:
            filter_list.append(Book.is_active == True)
            filter_list.append(Book.stock > 0)
        if key == "pub_year":
            filter_list.append(Book.publication_year == value)
        if key == "author":
            filter_list.append(Author.name.ilike(f"%{value}%"))
        if key == "category":
            filter_list.append(Category.title.ilike(f"%{value}%"))

    return filter_list
