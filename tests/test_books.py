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
            'ano': 1999,
            'titulo': 'test1',
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['id'] == 1


def test_create_book_with_conflict(
    client: TestClient,
    users: list[dict[str, str]],
    books: list[dict[str, str | int]],
):
    response = client.post(
        '/livro/',
        headers={'Authorization': f'bearer {users[1]["token"]}'},
        json={
            'ano': 1999,
            'titulo': 'livro1',
            'romancista_id': 1,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'livro.titulo já consta no MADR'


def test_get_book_by_id(client: TestClient, books: list[dict[str, str | int]]):
    response = client.get(
        '/livro/1',
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    books[0].pop('id')

    assert data == books[0]


def test_get_book_by_id_not_found(
    client: TestClient,
):
    response = client.get(
        '/livro/1',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Livro não consta no MADR'


def test_get_books_by_filter(
    client: TestClient, books: list[dict[str, str | int]]
):
    response = client.get('/livro/?titulo=livr')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['livros'] == books


def test_get_books_by_filter_empyt_return(
    client: TestClient, books: list[dict[str, str | int]]
):
    response = client.get('/livro/?ano=2000')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['livros'] == []


def test_update_book(
    client: TestClient,
    users: list[dict[str, str | int]],
    novelists: list[dict[str, str | int]],
    books: list[dict[str, str | int]],
):
    ano_test = 2000

    response = client.patch(
        'livro/1',
        headers={'Authorization': f'bearer {users[0]["token"]}'},
        json={
            'ano': ano_test,
            'titulo': 'Test',
            'romancista_id': novelists[1]['id'],
        },
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['ano'] == ano_test
    assert data['titulo'] == 'test'


def test_update_book_not_found(
    client: TestClient,
    users: list[dict[str, str | int]],
):
    ano_test = 2000

    response = client.patch(
        'livro/1',
        headers={'Authorization': f'bearer {users[0]["token"]}'},
        json={'ano': ano_test, 'titulo': 'Test'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Livro não consta no MADR'


def test_update_book_with_conflict(
    client: TestClient,
    users: list[dict[str, str | int]],
    books: list[dict[str, str | int]],
):
    ano_test = 2000

    response = client.patch(
        'livro/1',
        headers={'Authorization': f'bearer {users[0]["token"]}'},
        json={'ano': ano_test, 'titulo': 'Livro2'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'book.titulo já consta no MADR'


def test_delete_book(
    client: TestClient,
    users: list[dict[str, str | int]],
    books: list[dict[str, str | int]],
):
    response = client.delete(
        '/livro/1', headers={'Authorization': f'bearer {users[0]["token"]}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Livro deletado no MADR'


def test_delete_book_not_found(
    client: TestClient,
    users: list[dict[str, str | int]],
):
    response = client.delete(
        '/livro/1', headers={'Authorization': f'bearer {users[0]["token"]}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Livro não consta no MADR'
