from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    title: str
    parent_id: int | None = Field(default=None, ge=1)


class CategoryUpdateRequest(CategoryRequest):
    title: str | None = None
