from pydantic import BaseModel, Field, field_validator


class UserRoleUpdateRequest(BaseModel):
    role_slug: str
