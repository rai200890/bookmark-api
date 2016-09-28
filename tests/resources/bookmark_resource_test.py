import pytest
import json
from bookmark_api import db
from bookmark_api.models import Bookmark, User


@pytest.fixture
def user():
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("farofa")
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture
def user_2():
    user = User(username="raquel", email="raquel@email.com")
    user.hash_password("farofa2")
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture
def bookmark(user):
    bookmark = Bookmark(url="http://google.com", title="Google", user=user)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


@pytest.fixture
def valid_params(user):
    return {
        "title": "Google",
        "url": "http://google.com",
        "user_id": user.id
    }


@pytest.fixture
def invalid_params_duplicated(user_2):
    return {
        "title": "Google",
        "url": "http://google.com",
        "user_id": user_2.id
    }


@pytest.fixture
def invalid_params():
    return {
        "title": "DuckDuckGo"
    }


def test_get_exists(api_test_client, bookmark):
    response = api_test_client.get('/bookmarks/{}'.format(bookmark.id))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_get_doesnt_exists(api_test_client):
    response = api_test_client.get('/bookmarks/{}'.format(1))
    assert response.status_code == 404


def test_delete_exists(api_test_client, bookmark):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark.id))
    assert response.status_code == 204


def test_delete_doesnt_exists(api_test_client):
    response = api_test_client.delete('/bookmarks/{}'.format(1))
    assert response.status_code == 422


def test_post_valid(api_test_client, valid_params):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps({"bookmark": valid_params}),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_post_invalid_unique_url(api_test_client, bookmark, invalid_params_duplicated):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps({"bookmark": invalid_params_duplicated}),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_post_invalid_missing_fields(api_test_client, invalid_params):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps({"bookmark": invalid_params}),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_put_valid(api_test_client, bookmark, valid_params):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark.id),
                                   data=json.dumps({"bookmark": valid_params}),
                                   headers={'Content-Type': 'application/json'})
    assert response.status_code == 204


def test_put_invalid(api_test_client, bookmark, invalid_params):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark.id),
                                   data=json.dumps({"bookmark": invalid_params}),
                                   headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422
