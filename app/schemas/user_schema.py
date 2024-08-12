from pydantic import BaseModel, EmailStr,Field
from app.schemas.post_schema import Post
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    

# password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class UserCreate(UserBase):
    password: str 
    # = Field(...,regex=)



class User(UserBase):
    id: int 
    is_verified : bool = False
    is_superuser : bool = False
    is_firstlogin : bool = False
    created_at : datetime
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

class RefreshToken(BaseModel):
    refresh_token: str
    
