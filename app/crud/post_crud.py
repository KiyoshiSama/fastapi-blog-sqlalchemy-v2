from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post_model import Post
from app.schemas import PostBase, PostPUpdate


async def get_all(user, db: AsyncSession):
    result = await db.execute(
        select(Post).options(selectinload(Post.user)).filter(Post.user_id == user.id)
    )
    return result.scalars().all()


async def create(user, request, db):
    new_blog = Post(**request.model_dump(), user_id=user.id)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


async def destroy(id, db):
    result = await db.execute(select(Post).filter(Post.id == id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    await db.delete(blog)
    await db.commit()
    return JSONResponse({"detail": "blog post succefully deleted"})


async def update(id, request: PostBase, db):
    result = await db.execute(select(Post).filter(Post.id == id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    for key, value in request.model_dump().items():
        setattr(blog, key, value)

    await db.commit()
    await db.refresh(blog)
    return blog


async def partial_update(id, request: PostPUpdate, db):
    result = await db.execute(select(Post).filter(Post.id == id))
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(blog, key, value)

    await db.commit()
    await db.refresh(blog)
    return blog


async def retrieve_post(id, db):
    result = await db.execute(
        select(Post).options(selectinload(Post.user)).filter(Post.id == id)
    )
    blog = result.scalar_one_or_none()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return blog
