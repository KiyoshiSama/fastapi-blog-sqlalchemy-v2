
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import auth_handler, auth_utils
from app.database import get_db
from app.schemas.user_schema import Token

router = APIRouter()

@router.post("/login", response_model=Token)
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
    return {"access_token": access_token, "token_type": "bearer"}
