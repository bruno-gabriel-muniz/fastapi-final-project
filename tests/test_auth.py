from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


def test_get_access_token(
    client: TestClient, session: AsyncSession, users: list[dict[str, str]]
):
    response = client.post(
        '/auth/',
        data={'username': users[0]['email'], 'password': users[0]['password']},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'access_token' in data
    assert 'token_type' in data


def test_get_access_token_Not_Found_User(
    client: TestClient, session: AsyncSession, users: list[dict[str, str]]
):
    response = client.post(
        '/auth/',
        data={'username': 'Bob@example.com', 'password': users[1]['password']},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User Not Found'


def test_get_access_token_Icorrect(
    client: TestClient, session: AsyncSession, users: list[dict[str, str]]
):
    response = client.post(
        '/auth/',
        data={'username': users[1]['email'], 'password': 'NotSecret'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'User Or Password Incorrect'
