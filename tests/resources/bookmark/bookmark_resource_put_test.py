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


@pytest.fixture
def edit_valid_params():
    return {
        "bookmark": {
            "url": "http://google.com.br"
        }
    }


def test_put_bookmark_current_client(api_test_client, bookmark_current_client, edit_valid_params, client_auth_headers):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark_current_client.id),
                                   data=json.dumps(edit_valid_params),
                                   headers=client_auth_headers)
    b = Bookmark.query.get(bookmark_current_client.id)
    assert b.url == edit_valid_params["bookmark"]["url"]
    assert response.status_code == 204


def test_put_bookmark_from_other_user(api_test_client, bookmark_other_client, edit_valid_params, client_auth_headers):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark_other_client.id),
                                   data=json.dumps(edit_valid_params),
                                   headers=client_auth_headers)
    assert response.status_code == 403


def test_put_user_not_authenticated(api_test_client, bookmark_current_client, edit_valid_params):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark_current_client.id),
                                   data=json.dumps(edit_valid_params),
                                   headers={"content-type": "application/json"})
    assert response.status_code == 401
