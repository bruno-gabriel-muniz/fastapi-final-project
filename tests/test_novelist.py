from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tcc_madrs.models import Novelist


def test_create_novelist(client: TestClient, users: list[dict[str, str]]):
    response = client.post(
        '/romancista/',
        headers={'Authorization': f'Bearer {users[0]["token"]}'},
        json={
            'name': 'Teste',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['name'] == 'teste'
    assert data['id'] == 1


def test_create_novelist_conf(
    client: TestClient, users: list[dict[str, str]], novelist: Novelist
):
    response = client.post(
        '/romancista/',
        headers={'Authorization': f'Bearer {users[1]["token"]}'},
        json={'name': 'test1'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'romancista já consta no MADR'


@pytest.mark.asyncio
async def test_delete_novelist(
    client: TestClient,
    users: list[dict[str, str]],
    session: AsyncSession,
    novelist: Novelist,
):
    response = client.delete(
        '/romancista/1',
        headers={'Authorization': f'Bearer {users[0]["token"]}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Romancista deletada no MADR'

    novelist_in_db = await session.scalar(
        select(Novelist).where(Novelist.id == novelist.id)
    )

    assert novelist_in_db is None


def test_delete_novelist_not_found(
    client: TestClient, users: list[dict[str, str]]
):
    response = client.delete(
        '/romancista/1',
        headers={'Authorization': f'Bearer {users[0]["token"]}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Romancista não encontrado no MADR'


def test_get_novelist_id(
    client: TestClient,
    novelist: Novelist,
):
    response = client.get(
        '/romancista/1',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'test1'


def test_get_novelist_id_not_found(
    client: TestClient
):
    response = client.get(
        '/romancista/1',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Romancista não consta no MADR'


def test_get_novelist_by_filter(
    client: TestClient,
    novelists: list[dict[str, str | int]],
):
    response = client.get(
        '/romancista/?name=t',
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['romancistas'] == novelists


def test_get_novelist_by_filter_without_novelist_valid(
    client: TestClient,
    novelists: list[dict[str, str | int]],
):
    response = client.get(
        '/romancista/?name=a',
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['romancistas'] == []
