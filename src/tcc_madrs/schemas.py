from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int


class NovelistInput(BaseModel):
    name: str


class NovelistDB(NovelistInput):
    id: int


class FilterPage(BaseModel):
    limit: int = 20
    offset: int = 0


class FilterNovelist(FilterPage):
    name: str | None = None


class ListNovelist(BaseModel):
    romancistas: list[NovelistDB] = []


class BookInput(BaseModel):
    ano: int
    titulo: str
    romancista_id: int


class BookDB(BookInput):
    id: int


class BookPatch(BaseModel):
    ano: int | None = None
    titulo: str | None = None
    romancista_id: int | None = None


class FilterBooks(FilterPage):
    titulo: str | None = None
    ano: int | None = None


class ListBookDB(BaseModel):
    livros: list[BookDB]


class Token(BaseModel):
    access_token: str
    token_type: str
