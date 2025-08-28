from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.models import User


def test_post_conta(client: TestClient):
    response = client.post(
        '/conta/',
        json={
            'username': 'Alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['username'] == 'alice'
    assert data['email'] == 'alice@example.com'


def test_post_conta_conflit(client: TestClient, users: list[dict[str, str]]):
    response = client.post(
        '/conta/',
        json={
            'username': 'Alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data['detail'] == 'Email or UserName Alredy Exist'


def test_update_conta(client: TestClient, users: list[dict[str, str]]):
    response = client.put(
        '/conta/1',
        headers={'Authorization': f'Bearer {users[0]["token"]}'},
        json={
            'username': 'Alice test',
            'email': users[0]['email'],
            'password': users[0]['password'],
        },
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['username'] == 'alice test'


def test_update_conta_conflit(client: TestClient, users: list[dict[str, str]]):
    response = client.put(
        '/conta/2',
        headers={'Authorization': f'Bearer {users[1]["token"]}'},
        json={
            'username': 'Alice',
            'email': users[1]['email'],
            'password': users[1]['password'],
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'email ou username já consta no MADR'


def test_update_conta_forbidden(
    client: TestClient, users: list[dict[str, str]]
):
    response = client.put(
        '/conta/1',
        headers={'Authorization': f'Bearer {users[1]["token"]}'},
        json={
            'username': 'alice',
            'email': users[1]['email'],
            'password': users[1]['password'],
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert (
        response.json()['detail']
        == 'Alterações em outras contas não são permitadas'
    )


@pytest.mark.asyncio
async def test_delete_conta(
    client: TestClient, users: list[dict[str, str]], session: AsyncSession
):
    response = client.delete(
        '/conta/1', headers={'Authorization': f'Bearer {users[0]["token"]}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Conta deletada com sucesso'

    user_exist = await session.scalar(select(User).where(User.id == 1))

    assert user_exist is None


def test_delete_conta_forbidden(
    client: TestClient, users: list[dict[str, str]]
):
    response = client.delete(
        '/conta/1', headers={'Authorization': f'Bearer {users[1]["token"]}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert (
        response.json()['detail'] == 'Deleção de outras contas não permitido'
    )
