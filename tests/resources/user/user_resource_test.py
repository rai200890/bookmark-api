import json
import pytest

from bookmark_api.models import User


def test_get_exists(api_test_client, admin, admin_auth_headers):
    response = api_test_client.get('/users/{}'.format(admin.id), headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_get_doesnt_exist(api_test_client, admin_auth_headers):
    response = api_test_client.get('/users/{}'.format(0), headers=admin_auth_headers)
    assert response.status_code == 404


def test_delete_exists(session, api_test_client, admin_auth_headers, client_role):
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("aaaa")
    user.role = client_role
    session.add(user)
    session.flush()

    response = api_test_client.delete('/users/{}'.format(user.id), headers=admin_auth_headers)
    assert response.status_code == 204


def test_delete_doesnt_exists(api_test_client, admin_auth_headers):
    response = api_test_client.delete('/users/{}'.format(0), headers=admin_auth_headers)
    assert response.status_code == 422


def test_post_valid(api_test_client, create_valid_params, admin_auth_headers):
    response = api_test_client.post('/users',
                                    data=json.dumps(create_valid_params),
                                    headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_post_invalid(api_test_client, create_invalid_params, admin_auth_headers):
    response = api_test_client.post('/users',
                                    data=json.dumps(create_invalid_params),
                                    headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_put_valid(session, api_test_client, edit_valid_params, admin_auth_headers, client_role):
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("aaaa")
    user.role = client_role
    session.add(user)
    session.flush()

    response = api_test_client.put('/users/{}'.format(user.id),
                                   data=json.dumps(edit_valid_params),
                                   headers=admin_auth_headers)
    assert response.status_code == 204


@pytest.mark.skip
def test_put_invalid(session, api_test_client, edit_invalid_params, admin_auth_headers, client_role):
    user = User(username="raissaa", email="raissaa@email.com")
    user.hash_password("aaaa")
    user.role = client_role
    session.add(user)

    other_user = User(username="john_doee", email="john_doee@email.com")
    other_user.hash_password("aaaa")
    other_user.role = client_role
    session.add(user)

    session.flush()

    response = api_test_client.put('/users/{}'.format(other_user.id),
                                   data=json.dumps(edit_invalid_params),
                                   headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422
