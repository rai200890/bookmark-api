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
def other_user():
    user = User(username="john_doe", email="john_doe@email.com")
    user.hash_password("unknown")
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
def create_valid_params(role):
    return {
        "user": {
            "username": "john_doe",
            "email": "john_doe@email.com",
            "password": "unknown",
            "role_id": role.id
        }
    }


@pytest.fixture
def create_invalid_params():
    return {
        "user": {
            "username": "john_doe",
            "email": "john_doe@email.com",
        }
    }


@pytest.fixture
def edit_valid_params(role):
    return {
        "user": {"password": "unknown2"}
    }


@pytest.fixture
def edit_invalid_params(role, other_user):
    return {
        "user": {"email": "raissa@email.com"}
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


def test_post_valid(api_test_client, create_valid_params):
    response = api_test_client.post('/users',
                                    data=json.dumps(create_valid_params),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_post_invalid(api_test_client, create_invalid_params):
    response = api_test_client.post('/users',
                                    data=json.dumps(create_invalid_params),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_put_valid(api_test_client, user, edit_valid_params):
    response = api_test_client.put('/users/{}'.format(user.id),
                                   data=json.dumps(edit_valid_params),
                                   headers={'Content-Type': 'application/json'})
    assert response.status_code == 204


def test_put_invalid(api_test_client, user, other_user, edit_invalid_params):
    response = api_test_client.put('/users/{}'.format(other_user.id),
                                   data=json.dumps(edit_invalid_params),
                                   headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422
