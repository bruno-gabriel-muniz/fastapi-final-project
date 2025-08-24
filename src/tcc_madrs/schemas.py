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


# class Book(BaseModel):
#     ano: int
#     nome: str
#     romancista_id: int
#     id: int


class Token(BaseModel):
    access_token: str
    token_type: str
