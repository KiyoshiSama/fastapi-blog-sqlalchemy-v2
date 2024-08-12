import asyncio
from contextlib import ExitStack
from fastapi.testclient import TestClient
import pytest
from app import init_app
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from app.dependencies import get_db
from app.database import sessionmanager
from app.models import User, Post
from app.utils.auth_utils import get_password_hash
from datetime import datetime


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
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    # Initialize DatabaseJanitor with the correct signature
    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=test_db.version,
        password=pg_password,
    ):
        connection_str = (
            f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        )
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    # Create all tables before running tests
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)  # Drop all tables if needed
        await sessionmanager.create_all(connection)  # Create all tables


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


@pytest.fixture
async def test_user(client):
    async with sessionmanager.session() as session:
        hashed_password = get_password_hash("testpassword")
        new_user = User(
            email="testuser@example.com",
            password=hashed_password,
            first_name="Test",
            last_name="User",
            is_verified=True,
            is_firstlogin=False,
            is_superuser=False,
            created_at=datetime.now(),
        )
        session.add(new_user)
        await session.commit()

    # Log in the user to get the access token
    response = client.post(
        "/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    yield {"email": "testuser@example.com", "access_token": access_token}


@pytest.fixture
async def test_post(client):
    async with sessionmanager.session() as session:
        new_post = Post(
            title="post title test original",
            content="post content test",
            is_published=True,
            user_id=1,
            created_at=datetime.now(),
        )
        session.add(new_post)
        await session.commit()

        yield {
            "title": "post title test original",
            "content": "post content test",
            "is_published": True,
        }
