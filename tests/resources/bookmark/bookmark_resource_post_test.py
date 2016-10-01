import json

import pytest

@pytest.fixture
def create_valid_params():
    return {
        "bookmark": {
            "title": "Google",
            "url": "http://google.com"
        }
    }


@pytest.fixture
def create_invalid_params_missing():
    return {
        "bookmark": {
            "title": "Google"
        }
    }


def test_post_valid(api_test_client, create_valid_params, client_auth_headers):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_valid_params),
                                    headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_post_invalid_params_missing(api_test_client, create_invalid_params_missing, client_auth_headers):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_invalid_params_missing),
                                    headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422
