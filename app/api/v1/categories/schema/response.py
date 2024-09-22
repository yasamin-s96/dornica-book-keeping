from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    title: str | None = None
    parent_id: int | None = None

    class Config:
        orm_mode = True
