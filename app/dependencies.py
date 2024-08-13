from app.config import Config
from app.database import sessionmanager
import redis


def get_redis():
    pool = Config.create_redis()
    return redis.Redis(connection_pool=pool)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
