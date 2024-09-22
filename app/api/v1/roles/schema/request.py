from pydantic import BaseModel, Field, field_validator


class RoleRequest(BaseModel):
    name: str
    slug: str


class RoleUpdateRequest(BaseModel):
    name: str | None = None
    slug: str | None = None
