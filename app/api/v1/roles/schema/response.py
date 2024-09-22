from pydantic import BaseModel, Field, field_validator


class RoleResponse(BaseModel):
    id: int
    slug: str

    class Config:
        orm_mode = True
