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
from src.tcc_madrs.models import Book, Novelist, User, table_registry
from src.tcc_madrs.security import get_password_hash
from src.tcc_madrs.settings import Settings


@pytest.fixture
def settings() -> Settings:
    return Settings()  # type: ignore


@pytest.fixture
def client(session: AsyncSession):
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
async def users(
    session: AsyncSession, settings: Settings
) -> list[dict[str, str]]:
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
def fake_token(settings: Settings) -> str:
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
def fake_token_without_sub(settings: Settings) -> str:
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
async def novelist(session: AsyncSession) -> Novelist:
    novelist1 = Novelist('test1')

    session.add(novelist1)
    await session.commit()
    await session.refresh(novelist1)

    return novelist1


@pytest_asyncio.fixture
async def novelists(session: AsyncSession) -> list[dict[str, str | int]]:
    novelist1 = Novelist('test1')
    novelist2 = Novelist('test2')
    novelist3 = Novelist('test3')

    session.add(novelist1)
    session.add(novelist2)
    session.add(novelist3)

    await session.commit()

    list_novelist = [
        {'name': 'test1', 'id': 1},
        {'name': 'test2', 'id': 2},
        {'name': 'test3', 'id': 3},
    ]

    return list_novelist


@pytest_asyncio.fixture
async def books(session: AsyncSession) -> list[dict[str, str | int]]:
    book1 = Book(1999, 'livro1', 1)
    book2 = Book(1999, 'livro2', 2)
    book3 = Book(1999, 'livro3', 3)

    session.add_all([book1, book2, book3])

    await session.commit()

    return [
        {'year': 1999, 'name': 'livro1', 'romancista_id': 1, 'id': 1},
        {'year': 1999, 'name': 'livro2', 'romancista_id': 2, 'id': 2},
        {'year': 1999, 'name': 'livro3', 'romancista_id': 3, 'id': 3},
    ]
