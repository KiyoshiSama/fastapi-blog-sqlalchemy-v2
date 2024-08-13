from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User as UserModel
from app.schemas.user_schema import UserBase, UserPUpdate
from app.utils import auth_utils
from sqlalchemy.orm import selectinload


async def get_all(db: AsyncSession):
    result = await db.execute(select(UserModel).options(selectinload(UserModel.posts)))
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    for key, value in request.model_dump().items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def partial_update(id: int, request: UserPUpdate, db: AsyncSession):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def destroy(id, db):
    result = await db.execute(select(UserModel).filter(UserModel.id == id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    await db.delete(user)
    await db.commit()
    return JSONResponse({"detail": "User succefully deleted"})


async def retrieve_user(id: int, db: AsyncSession):
    result = await db.execute(
        select(UserModel)
        .options(selectinload(UserModel.posts))
        .filter(UserModel.id == id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user
