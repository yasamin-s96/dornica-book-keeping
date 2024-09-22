from pydantic import BaseModel


class AuthorRequest(BaseModel):
    name: str
    nationality: str | None = None


class AuthorUpdateRequest(AuthorRequest):
    name: str | None = None
