import random
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import (
    User,
    UserCreate,
    UserBase,
    UserVerifyCode,
    TokenData,
)
from app.models import User as UserModel
from app.database import get_db
from app.crud import user
from app.auth import auth_handler
from app.utils import email
from app.dependencies import get_reddis
from app.auth.auth_handler import get_current_user


router = APIRouter(prefix="/user", tags=["Users"])


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[User],
)
async def all(db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    return await user.get_all(db)


@router.get("/users/me")
async def read_users_me(
    current_user: TokenData = Depends(auth_handler.get_current_user),
):
    return current_user


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    request: UserCreate,
    background_tasks: BackgroundTasks,
    cache=Depends(get_reddis),
    db: AsyncSession = Depends(get_db),
):
    created_user = await user.create(request, db)
    # await email.send_email_async("Welcome aboard",created_user.email,{"first_name": created_user.first_name })
    verification_code = str(random.randint(10000, 99999))
    cache.set(str(created_user.email), verification_code, 600)
    email.send_email_background(
        background_tasks,
        "Your account verficiation code",
        created_user.email,
        {"first_name": created_user.first_name, "activation_code": verification_code},
    )
    return {
        "detail": "your account has been created succefully, please check your email!"
    }


@router.post(
    "/activate-account",
    status_code=status.HTTP_200_OK,
)
async def activate(
    request: UserVerifyCode,
    cache=Depends(get_reddis),
    db: AsyncSession = Depends(get_db),
):
    user = await db.execute(select(UserModel).filter(UserModel.email == request.email))
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    if user.is_firstlogin:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You've already activated your account"
        )
    cached_code = cache.get(request.email)
    if request.code != cached_code:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="code has expired"
        )

    user.is_verified = True
    user.is_firstlogin = False
    await db.commit()
    await db.refresh(user)
    return {"details": "account confirmed sucessfully"}


@router.patch(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(id: int, request: UserBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    return await user.update(id, request, db)


@router.get(
    "/{id}",
    status_code=200,
    response_model=User,
)
async def show(id: int, db: AsyncSession = Depends(get_db)):
    return await user.show(id, db)
