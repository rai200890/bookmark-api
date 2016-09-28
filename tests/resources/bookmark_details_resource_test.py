import pytest
import json
from bookmark_api import db
from bookmark_api.models import Bookmark, User


@pytest.fixture(autouse=True)
def bookmark():
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("farofa")
    db.session.add(user)
    bookmark = Bookmark(url="http://google.com", title="Google", user=user)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


def test_bookmark_details_get_exists(api_test_client, bookmark):
    response = api_test_client.get('/bookmarks/{}'.format(bookmark.id))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_bookmark_details_get_doesnt_exists(api_test_client):
    response = api_test_client.get('/bookmarks/{}'.format(1))
    assert response.status_code == 404


def test_bookmark_details_delete_exists(api_test_client, bookmark):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark.id))
    assert response.status_code == 204


def test_bookmark_details_delete_doesnt_exists(api_test_client):
    response = api_test_client.delete('/bookmarks/{}'.format(1))
    assert response.status_code == 422
