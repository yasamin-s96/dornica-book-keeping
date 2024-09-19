from pydantic import BaseModel, Field


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category: str
    stock: int
    publication_year: int
    image_urls: list[str]


class BookRawResponse(BaseModel):
    id: int
    title: str
    author_id: int
    category_id: int
    publication_year: int
    stock: int
    is_active: bool

    class Config:
        orm_mode = True
