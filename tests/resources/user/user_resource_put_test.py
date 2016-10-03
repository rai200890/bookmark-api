import json
import pytest


@pytest.fixture
def edit_valid_params():
    return {
        "user": {"password": "unknown2"}
    }


def test_put_valid(api_test_client, edit_valid_params, client, admin, client_auth_headers):
    response = api_test_client.put('/users/{}'.format(client.id),
                                   data=json.dumps(edit_valid_params),
                                   headers=client_auth_headers)
    assert response.status_code == 204
