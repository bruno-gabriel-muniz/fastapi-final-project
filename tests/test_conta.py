from http import HTTPStatus

from fastapi.testclient import TestClient


def test_post_user(client: TestClient):
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


def test_post_user_conflit(client: TestClient, users: list[dict[str, str]]):
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


def test_update_user(client, users):
    response = client.put(
        '/conta/1',
        headers={'Authorization': f'Bearer {users[0]["token"]}'},
        json={
            'username': 'Alice',
            'email': users[0]['email'],
            'password': users[0]['password'],
        },
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['username'] == 'Alice'


def test_update_user_conflit(client, users):
    response = client.put(
        '/conta/2',
        headers={'Authorization': f'Bearer {users[1]["token"]}'},
        json={
            'username': 'alice',
            'email': users[1]['email'],
            'password': users[1]['password'],
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'email ou username já consta no MADR'


def test_update_user_forbidden(client, users):
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
