import redis
from decouple import config


class Config:
    DB_CONFIG = config("DATABASE_URL",default="postgresql+asyncpg://amirh:784512@localhost/blog")


    @staticmethod
    def create_redis():
        return redis.ConnectionPool(
            host="localhost", port=6379, db=0, decode_responses=True
        )


config = Config()
