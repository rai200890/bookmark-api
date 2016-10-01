from bookmark_api.models import Bookmark


def test_delete_exists(api_test_client, bookmark, client_auth_headers):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark.id), headers=client_auth_headers)
    assert Bookmark.query.filter_by(id=bookmark.id).count() == 0
    assert response.status_code == 204


def test_delete_doesnt_exist(api_test_client, bookmark, client_auth_headers):
    Bookmark.query.filter_by(id=bookmark.id).delete()
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark.id), headers=client_auth_headers)
    assert response.status_code == 422
