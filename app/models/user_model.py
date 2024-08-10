from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from datetime import datetime
from . import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post_model import Post

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_firstlogin: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
