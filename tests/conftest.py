from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from jwt import encode
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from src.tcc_madrs.app import app
from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import Novelist, User, table_registry
from src.tcc_madrs.security import get_password_hash
from src.tcc_madrs.settings import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings()  # type: ignore


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def users(session, settings) -> list[dict[str, str]]:
    # Cria os usuários
    password_hashed = get_password_hash('secret')

    alice = User('alice', 'alice@example.com', password_hashed)
    token_alice = encode(
        {
            'sub': 'alice@example.com',
            'exp': datetime.now(ZoneInfo('UTC')) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )
    bob = User('bob', 'bob@example.com', password_hashed)
    token_bob = encode(
        {
            'sub': 'bob@example.com',
            'exp': datetime.now(ZoneInfo('UTC')) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    # Cria a cunsulta dos dados deles
    out = [
        {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
            'token': token_alice,
        },
        {
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
            'token': token_bob,
        },
    ]

    session.add(alice)
    session.add(bob)
    await session.commit()

    return out


@pytest.fixture
def fake_token(settings) -> str:
    fk_token = encode(
        {
            'sub': 'Bob@example.com',
            'exp': datetime.now(ZoneInfo('UTC')) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )
    return fk_token


@pytest.fixture
def fake_token_without_sub(settings) -> str:
    fake_token = encode(
        {
            # 'sub': 'Bob@example.com',
            'exp': datetime.now(ZoneInfo('UTC')) + timedelta(minutes=5),
        },
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return fake_token


@pytest_asyncio.fixture
async def novelist(session) -> Novelist:
    novelist1 = Novelist('test1')

    session.add(novelist1)
    await session.commit()
    await session.refresh(novelist1)

    return novelist1
