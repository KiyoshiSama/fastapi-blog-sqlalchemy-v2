
import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.testing.entities import ComparableEntity
from app.config import Config
from app.api import init_app
from app.models import User
from app.database import sessionmanager
from app.dependencies import get_db


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):

    with DatabaseJanitor(
    ):
        # connection_str = "postgresql+asyncpg://amirh:784512@localhost/blog"
        # connection_str = Config.DB_CONFIG

        sessionmanager.init(Config.DB_CONFIG)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override
