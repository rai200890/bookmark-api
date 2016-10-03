import json


def test_user_list_get_admin(api_test_client, admin_auth_headers):
    response = api_test_client.get('/users', headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data['users']) == 3


def test_user_list_get_client(api_test_client, client_auth_headers):
    response = api_test_client.get('/users', headers=client_auth_headers)
    assert response.status_code == 403
