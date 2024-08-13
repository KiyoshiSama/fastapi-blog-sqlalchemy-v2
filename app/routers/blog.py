from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post_schema import PostResponse, PostBase, PostPUpdate
from app.dependencies import get_db
from app.crud import post_crud
from app.utils.auth_handler import get_current_user
from app.schemas.user_schema import User

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse])
async def all_posts(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await post_crud.get_all(current_user, db)


@router.post("/", response_model=PostBase, status_code=status.HTTP_201_CREATED)
async def create(
    request: PostBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post_crud.create(current_user, request, db)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def destroy(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await post_crud.destroy(id, db)


@router.put("/{id}", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def update(
    id: int,
    request: PostBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post_crud.update(id, request, db)


@router.patch("/{id}", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def partial_update(
    id: int,
    request: PostPUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await post_crud.partial_update(id, request, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def retrieve(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await post_crud.retrieve_post(id, db)
