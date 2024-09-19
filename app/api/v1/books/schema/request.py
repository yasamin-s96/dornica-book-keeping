from pydantic import BaseModel, Field, field_validator
from khayyam import JalaliDatetime


class AddBookRequest(BaseModel):
    title: str
    author_id: int = Field(ge=1)
    category_id: int = Field(ge=1)
    publication_year: int = Field(ge=1000, le=JalaliDatetime.now().year)
    stock: int = Field(ge=0)
    image_ids: list[int] | None = None
    is_active: bool = Field(default=True)

    @field_validator("image_ids")
    @classmethod
    def validate_image_ids(cls, value: list[int]):
        if value is not None:
            for image_id in value:
                if image_id <= 0:
                    raise ValueError("مقادیر تصاویر باید بیشتر از 0 باشند.")
        return value


class UpdateBookRequest(AddBookRequest):
    title: str | None = None
    author_id: int | None = Field(ge=1, default=None)
    category_id: int | None = Field(ge=1, default=None)
    publication_year: int | None = Field(
        ge=1000, le=JalaliDatetime.now().year, default=None
    )
    stock: int | None = Field(ge=0, default=None)
    image_ids: list[int] | None = None
    is_active: bool | None = Field(default=True)
