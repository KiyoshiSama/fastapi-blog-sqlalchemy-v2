from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post_schema import Post, PostCreate, PostBase
from app.database import get_db
from app.crud import post
from app.auth.auth_handler import get_current_user
from app.schemas.user_schema import User

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/all", response_model=list[Post])
async def all(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await post.get_all(current_user, db)


@router.post(
    "/create-new", response_model=PostBase, status_code=status.HTTP_201_CREATED
)
async def create(
    request: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post.create(current_user, request, db)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post.destroy(id, db)


@router.put("/update/{id}", response_model=Post, status_code=status.HTTP_202_ACCEPTED)
async def update(
    id: int,
    request: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post.update(id, request, db)


@router.get("/show/{id}", status_code=200, response_model=Post)
async def show(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post.show(id, db)
