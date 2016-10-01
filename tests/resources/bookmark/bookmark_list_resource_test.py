import json
import pytest

from bookmark_api import db
from bookmark_api.models import Bookmark


@pytest.fixture
def bookmark_current_client(client):
    bookmark = Bookmark(url="http://google.com", title="Google", user=client)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


@pytest.fixture
def bookmark_other_client(other_client):
    bookmark = Bookmark(url="http://google.com", title="Google", user=other_client)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


def test_bookmark_list_client(api_test_client, bookmark_other_client, bookmark_current_client, client_auth_headers):
    response = api_test_client.get("/bookmarks?per_page=15&page=1", headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    bookmark_ids = [bookmark["id"] for bookmark in data['bookmarks']]
    assert bookmark_ids == [bookmark_current_client.id]
    assert data["pagination"] == {'has_prev': False, 'prev_page': 0, 'next_page': 2,
                                  'has_next': False, 'total': 1, 'pages': 1, 'per_page': 15}


def test_bookmark_list_admin(api_test_client, bookmark_current_client, bookmark_other_client, admin_auth_headers):
    response = api_test_client.get("/bookmarks?per_page=15&page=1", headers=admin_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    bookmark_ids = [bookmark["id"] for bookmark in data['bookmarks']]
    assert bookmark_ids == [bookmark_current_client.id, bookmark_other_client.id]
    assert data["pagination"] == {'has_prev': False, 'prev_page': 0, 'next_page': 2,
                                  'has_next': False, 'total': 2, 'pages': 1, 'per_page': 15}
