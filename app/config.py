import redis
from decouple import config as decouple_config


class Config:
    DB_CONFIG = decouple_config("DATABASE_URL")
    TEST_DB_CONFIG = decouple_config("TEST_DATABASE_URL")

    @staticmethod
    def create_redis():
        return redis.ConnectionPool(
            host=decouple_config("REDIS_HOST"), port=decouple_config("REDIS_PORT"), db=decouple_config("REDIS_DB"), decode_responses=True
        )


config = Config()
