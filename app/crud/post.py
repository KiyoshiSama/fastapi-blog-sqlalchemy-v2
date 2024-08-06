from sqlalchemy.orm import selectinload
from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post_model import Post as PostModel
from app.schemas.post_schema import  PostCreate
from fastapi import HTTPException


async def get_all(user, db: AsyncSession):
    result = await db.execute(
        select(PostModel)
        .options(selectinload(PostModel.user))
        .filter(PostModel.user_id == user.id)
    )
    return result.scalars().all()


async def create(user, request, db):
    new_blog = PostModel(**request.model_dump(), user_id=user.id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


async def destroy(id, db):
    result = await db.execute(select(PostModel).filter(PostModel.id == id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    await db.delete(blog)
    await db.commit()
    return {"detail": "blog post succefully deleted"}


async def update(id, request: PostCreate, db):
    result = await db.execute(select(PostModel).filter(PostModel.id == id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    for key, value in request.model_dump().items():
        setattr(blog, key, value)

    await db.commit()
    await db.refresh(blog)
    return blog


async def show(id, db):
    result = await db.execute(
        select(PostModel)
        .options(selectinload(PostModel.user))
        .filter(PostModel.id == id)
    )
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    return blog
