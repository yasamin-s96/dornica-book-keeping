from .request import AuthorRequest


class AuthorResponse(AuthorRequest):
    id: int

    class Config:
        orm_mode = True
