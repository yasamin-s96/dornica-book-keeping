from pydantic import BaseModel, Field, field_validator


class PermissionResponse(BaseModel):
    id: int
    slug: str

    class Config:
        orm_mode = True
