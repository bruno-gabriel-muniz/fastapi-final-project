from http import HTTPStatus


def test(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data == {'message': 'Hello Wolrd!'}
