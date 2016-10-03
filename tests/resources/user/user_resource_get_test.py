import json


def test_get_exists_admin(api_test_client, admin_auth_headers, admin):
    response = api_test_client.get('/users/{}'.format(admin.id), headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_get_exists_current_client(api_test_client, client, client_auth_headers):
    response = api_test_client.get('/users/{}'.format(client.id), headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['user']


def test_get_exists_other_client(api_test_client, client, other_client, client_auth_headers):
    response = api_test_client.get('/users/{}'.format(other_client.id), headers=client_auth_headers)
    assert response.status_code == 403


def test_get_doesnt_exist(api_test_client, admin_auth_headers):
    response = api_test_client.get('/users/{}'.format(0), headers=admin_auth_headers)
    assert response.status_code == 403
