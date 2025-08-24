from http import HTTPStatus

from fastapi.testclient import TestClient

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
