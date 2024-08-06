from __future__ import annotations
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str



class User(BaseModel):
    id: int 
    is_verified : bool = False
    is_superuser : bool = False
    is_firstlogin : bool = False
    blogs: list[Post] = []

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class Email(BaseModel):
    email: EmailStr

class UserVerifyCode(Email):
    code: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


from app.schemas.post_schema import Post
