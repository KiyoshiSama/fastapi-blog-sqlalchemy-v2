from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.blog import router as blog_router
from app.routers.authentication import router as auth_router
from app.database import sessionmanager
from app.config import Config


def init_app(init_db=True):
    lifespan = None

    if init_db:
        sessionmanager.init(Config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(title="FastAPI Blog", lifespan=lifespan, docs_url="/api/docs")

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(blog_router)

    return app
