from http import HTTPStatus


def test_post_user(client):
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


def test_post_user_conflit(client, users):
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
