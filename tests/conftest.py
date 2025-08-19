import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.tcc_madrs.app import app
from src.tcc_madrs.database import get_session
from src.tcc_madrs.models import User, table_registry
from src.tcc_madrs.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def users(session) -> list[dict[str, str]]:
    # Cria os usuários
    password_hashed = get_password_hash('secret')

    alice = User('alice', 'alice@example.com', password_hashed)
    bob = User('bob', 'bob@example.com', password_hashed)

    # Cria a cunsulta dos dados deles
    out = [
        {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
        {
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    ]

    session.add(alice)
    session.add(bob)
    await session.commit()

    return out
