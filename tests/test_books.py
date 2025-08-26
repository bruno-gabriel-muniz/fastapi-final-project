from http import HTTPStatus

from fastapi.testclient import TestClient


def test_create_book(
    client: TestClient,
    users: list[dict[str, str]],
    novelists: list[dict[str, str | int]],
):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'bearer {users[0]["token"]}'},
        json={
            'year': 1999,
            'name': 'test1',
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['id'] == 1


def test_create_book_with_conflict(
    client: TestClient,
    users: list[dict[str, str]],
    novelists: list[dict[str, str | int]],
    books: list[dict[str, str | int]],
):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'bearer {users[1]["token"]}'},
        json={
            'year': 1999,
            'name': 'livro1',
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'livro.name já consta no MADR'
