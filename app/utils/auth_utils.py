from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from app.models import User
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")


async def authenticate_user(request, db):
    result = await db.execute(select(User).where(User.email == request.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(request.password, user.password):
        return None
    return user


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_valid = pwd_context.verify(plain_password, hashed_password)
    return is_valid
