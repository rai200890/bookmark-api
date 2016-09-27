import pytest
import json
from bookmark_api import db
from bookmark_api.models import Bookmark, User


def setup_module():
    user = User(username="raissa")
    user.hash_password("farofa")
    db.session.add(user)
    bookmark = Bookmark(url="http://google.com", title="Google", user=user)
    db.session.add(bookmark)
    db.session.flush()


def test_bookmark_list_get(api_test_client):
    response = api_test_client.get('/bookmarks?page=1&per_page=15')
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data['bookmarks']) == 1
    assert data["pagination"] == {'has_prev': False, 'prev_page': 0, 'next_page': 2,
                                  'has_next': False, 'total': 1, 'pages': 1, 'per_page': 15}
