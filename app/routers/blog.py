from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post_schema import Post, PostCreate, PostBase
from app.dependencies import get_db
from app.crud import post_crud
from app.utils.auth_handler import get_current_user
from app.schemas.user_schema import User

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.get("/all", response_model=list[Post])
async def all(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await post_crud.get_all(current_user, db)


@router.post(
    "/create-new", response_model=PostBase, status_code=status.HTTP_201_CREATED
)
async def create(
    request: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post_crud.create(current_user, request, db)


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def destroy(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await post_crud.destroy(id, db)


@router.put("/update/{id}", response_model=Post, status_code=status.HTTP_201_CREATED)
async def update(
    id: int,
    request: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await post_crud.update(id, request, db)


@router.patch("/update/{id}", response_model=Post, status_code=status.HTTP_201_CREATED)
async def update(
    id: int,
    request: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await post_crud.partial_update(id, request, db)


@router.get("/show/{id}", status_code=status.HTTP_200_OK, response_model=Post)
async def retrieve(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await post_crud.retrieve_post(id, db)
