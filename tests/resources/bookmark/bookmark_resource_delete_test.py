import pytest

from bookmark_api.models import Bookmark
from bookmark_api import db


@pytest.fixture
def bookmark_from_current_client(client):
    bookmark = Bookmark(url="http://google.com", title="Google", user=client)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


@pytest.fixture
def bookmark_from_other_client(other_client):
    bookmark = Bookmark(url="http://google.com", title="Google", user=other_client)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


def test_delete_bookmark_from_current_client(api_test_client, bookmark_from_current_client, client_auth_headers):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark_from_current_client.id),
                                      headers=client_auth_headers)
    assert Bookmark.query.filter_by(id=bookmark_from_current_client.id).count() == 0
    assert response.status_code == 204


def test_delete_bookmark_from_other_client(api_test_client, bookmark_from_other_client, client_auth_headers):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark_from_other_client.id),
                                      headers=client_auth_headers)
    assert response.status_code == 403


def test_delete_bookmark_from_user_not_authenticated(api_test_client, bookmark_from_other_client):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark_from_other_client.id),
                                      headers={"content-type": "application/json"})
    assert response.status_code == 401
