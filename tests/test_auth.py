from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient
from freezegun import freeze_time
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


def test_refresh_access_token(client: TestClient, users: list[dict[str, str]]):
    response = client.post(
        '/auth/refresh/',
        headers={'Authorization': f'Bearer {users[0]["token"]}'},
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert 'token_type' in data
    assert 'access_token' in data


def test_refresh_access_token_Expired_time(
    client: TestClient, users: list[dict[str, str]]
):
    with freeze_time(datetime.now(ZoneInfo('UTC')) + timedelta(minutes=6)):
        response = client.post(
            '/auth/refresh/',
            headers={'Authorization': f'Bearer {users[0]["token"]}'},
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_refresh_access_token_Invalid(
    client: TestClient, users: list[dict[str, str]]
):
    response = client.post(
        '/auth/refresh/',
        headers={'Authorization': 'Bearer not_valid'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_refresh_access_token_Invalid_without_sub(
        client: TestClient, fake_token_without_sub
):
    response = client.post(
        '/auth/refresh/',
        headers={'Authorization': f'Bearer {fake_token_without_sub}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_refresh_access_token_Invalid_sub(
        client: TestClient, fake_token
):
    response = client.post(
        '/auth/refresh/',
        headers={'Authorization': f'Bearer {fake_token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'
