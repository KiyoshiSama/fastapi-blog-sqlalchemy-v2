
import asyncio
from contextlib import ExitStack
import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from ..api import app
from app.database import get_db, sessionmanager

@pytest.fixture
def client():
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
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = "postgresql+asyncpg://amirh:784512@localhost/blog"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()

@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)

@pytest.fixture(scope="function", autouse=True)
async def session_override():
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override
