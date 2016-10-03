import json

import pytest

from bookmark_api.models import Bookmark


@pytest.fixture
def bookmark_from_current_client(session, client):
    bookmark = Bookmark(url="http://google.com", title="Google", user=client)
    session.add(bookmark)
    session.flush()
    return bookmark


@pytest.fixture
def bookmark_from_other_client(session, other_client):
    bookmark = Bookmark(url="http://google.com", title="Google", user=other_client)
    session.add(bookmark)
    session.flush()
    return bookmark


def test_get_user_not_authenticated(api_test_client, bookmark_from_other_client):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark_from_other_client.id),
                                   headers={"content-type": "application/json"})
    assert response.status_code == 401


def test_get_bookmark_from_other_client(api_test_client, bookmark_from_other_client, client_auth_headers):
    response = api_test_client.get('/bookmarks/{}'.format(bookmark_from_other_client.id),
                                   headers=client_auth_headers)
    assert response.status_code == 403


def test_get_bookmark_from_current_client(api_test_client, bookmark_from_current_client, client_auth_headers):
    response = api_test_client.get('/bookmarks/{}'.format(bookmark_from_current_client.id),
                                   headers=client_auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_get_bookmark_doesnt_exist(api_test_client, client_auth_headers):
    response = api_test_client.get('/bookmarks/{}'.format(0), headers=client_auth_headers)
    assert response.status_code == 403
