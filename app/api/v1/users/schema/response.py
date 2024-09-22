from pydantic import BaseModel, Field, field_validator


class UserResponse(BaseModel):
    id: int
    email: str
    role_id: int

    class Config:
        orm_mode = True
