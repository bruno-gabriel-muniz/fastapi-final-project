import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

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


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def users(session) -> list[dict[str, str]]:
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
    session.commit()

    return out
