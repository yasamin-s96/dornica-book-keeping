from pydantic import BaseModel


class RolePermissionRequest(BaseModel):
    role_slug: str
    permission_slug: str
