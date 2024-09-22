from pydantic import BaseModel


class RolePermissionResponse(BaseModel):
    role_slug: str
    permission_slug: str
