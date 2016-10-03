import json

import pytest


@pytest.fixture
def create_valid_params():
    return {
        "user": {
            "username": "john_doe",
            "email": "john_doe@email.com",
            "password": "unknown",
            "role_id": 2
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


def test_post_valid(api_test_client, create_valid_params, client_auth_headers):
    response = api_test_client.post('/users',
                                    data=json.dumps(create_valid_params),
                                    headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_post_invalid(api_test_client, create_invalid_params, client_auth_headers):
    response = api_test_client.post('/users',
                                    data=json.dumps(create_invalid_params),
                                    headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422
