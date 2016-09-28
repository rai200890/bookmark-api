import pytest
import json
from bookmark_api import db
from bookmark_api.models import User, Role


@pytest.fixture
def user():
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("farofa")
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture
def role():
    role = Role(name="admin")
    db.session.add(role)
    db.session.flush()
    return role


@pytest.fixture
def valid_params(role):
    return {
        "username": "john_doe",
        "email": "john_doe@email.com",
        "password": "unknown",
        "role_id": role.id
    }


@pytest.fixture
def invalid_params():
    return {
        "username": "john_doe",
        "email": "john_doe@email.com",
    }


def test_get_exists(api_test_client, user):
    response = api_test_client.get('/users/{}'.format(user.id))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_get_doesnt_exist(api_test_client):
    response = api_test_client.get('/users/{}'.format(1))
    assert response.status_code == 404


def test_delete_exists(api_test_client, user):
    response = api_test_client.delete('/users/{}'.format(user.id))
    assert response.status_code == 204


def test_delete_doesnt_exists(api_test_client):
    response = api_test_client.delete('/users/{}'.format(1))
    assert response.status_code == 422


def test_post_valid(api_test_client, valid_params):
    response = api_test_client.post('/users',
                                    data=json.dumps({"user": valid_params}),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_post_invalid(api_test_client, invalid_params):
    response = api_test_client.post('/users',
                                    data=json.dumps({"user": invalid_params}),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_put_valid(api_test_client, user, valid_params):
    response = api_test_client.put('/users/{}'.format(user.id),
                                   data=json.dumps({"user": valid_params}),
                                   headers={'Content-Type': 'application/json'})
    assert response.status_code == 204


def test_put_invalid(api_test_client, user, invalid_params):
    response = api_test_client.put('/users/{}'.format(user.id),
                                   data=json.dumps({"user": invalid_params}),
                                   headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422
