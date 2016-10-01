import json


def test_user_list_get(api_test_client, admin_auth_headers):
    response = api_test_client.get('/users', headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data['users']) == 2
