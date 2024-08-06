import random
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User as UserModel
from app.schemas.user_schema import UserBase, UserCreate
from app.auth import auth_utils


async def get_all(db: AsyncSession):
    result = await db.execute(select(UserModel))
    return result.scalars().all()


async def create(request, db):

    new_user = UserModel(
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        password=auth_utils.get_password_hash(request.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update(id: int, request: UserBase, db: AsyncSession):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    for key, value in request.model_dump().items():
        setattr(user, key, value)
    await db.commit()
    return {"detail": "User succefully updated"}


async def show(id: int, db: AsyncSession):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user


