from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id : int
    created : datetime
    user_id : int
    class Config():
        orm_mode = True


