from pydantic import BaseModel, Field, field_validator


class PermissionRequest(BaseModel):
    name: str
    slug: str


class PermissionUpdateRequest(BaseModel):
    name: str | None = None
    slug: str | None = None
