from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool


class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True
