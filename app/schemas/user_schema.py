from pydantic import BaseModel, EmailStr, Field
from app.schemas.post_schema import PostResponse
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserPartialUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


# password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class UserCreate(UserBase):
    password: str
    # = Field(...,regex=)


class User(UserBase):
    id: int
    is_verified: bool = False
    is_superuser: bool = False
    is_firstlogin: bool = False
    created_at: datetime
    posts: list[PostResponse] = []

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
    id: int


class RefreshToken(BaseModel):
    refresh_token: str
