from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import auth_utils, auth_handler
from app.dependencies import get_db
from app.schemas.user_schema import RefreshToken, Login

router = APIRouter()


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await auth_utils.authenticate_user(request, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_handler.create_access_token(data={"sub": user.id})
    refresh_token = auth_handler.create_refresh_token(data={"sub": user.id})
    return JSONResponse(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/refresh")
async def refresh(request: RefreshToken, db: AsyncSession = Depends(get_db)):
    user_id = auth_handler.verify_refresh_token(request.refresh_token)
    access_token = auth_handler.create_access_token(data={"sub": user_id})

    return JSONResponse({"access": access_token}, status_code=status.HTTP_201_CREATED)
