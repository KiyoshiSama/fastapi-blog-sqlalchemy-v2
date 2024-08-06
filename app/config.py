import os
from decouple import config
class Config:
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://amirh:784512@localhost/blog"
    )


config = Config()