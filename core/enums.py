from enum import Enum


class RoleSlug(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class PermissionSlug(str, Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
