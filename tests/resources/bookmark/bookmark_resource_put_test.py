import json

import pytest

@pytest.fixture
def edit_valid_params():
    return {
        "bookmark": {
            "url": "http://google.com.br"
        }
    }


def test_put_valid(api_test_client, bookmark, edit_valid_params, client_auth_headers):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark.id),
                                   data=json.dumps(edit_valid_params),
                                   headers=client_auth_headers)
    assert response.status_code == 204
