from app.redis_db import pool
import redis


def get_reddis():
    return redis.Redis(connection_pool=pool)

