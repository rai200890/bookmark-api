import json

import pytest

from bookmark_api.models import Bookmark


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


def test_post_valid_from_client(api_test_client, create_valid_params, client_auth_headers):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_valid_params),
                                    headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 201
    assert data['bookmark']['id']
    assert Bookmark.query.filter_by(**create_valid_params['bookmark']).count() == 1


def test_post_invalid_params_missing(api_test_client, create_invalid_params_missing, client_auth_headers):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_invalid_params_missing),
                                    headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_post_from_admin(api_test_client, create_valid_params, admin_auth_headers):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_valid_params),
                                    headers=admin_auth_headers)
    assert response.status_code == 403
