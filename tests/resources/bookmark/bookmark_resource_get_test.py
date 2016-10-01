import json


def test_get_exists(api_test_client, bookmark, client_auth_headers):
    response = api_test_client.get('/bookmarks/{}'.format(bookmark.id), headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_get_doesnt_exist(api_test_client, client_auth_headers):
    response = api_test_client.get('/bookmarks/{}'.format(0), headers=client_auth_headers)
    assert response.status_code == 404
