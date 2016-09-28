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
def bookmark(user):
    bookmark = Bookmark(url="http://google.com", title="Google", user=user)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


@pytest.fixture
def other_bookmark(user):
    bookmark = Bookmark(url="http://google.com", title="Search", user=user)
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


@pytest.fixture
def create_valid_params(user):
    return {
        "bookmark": {
            "title": "Google",
            "url": "http://google.com",
            "user_id": user.id
        }
    }


@pytest.fixture
def create_invalid_params_duplicated_url(user):
    return {
        "bookmark": {
            "title": "Google",
            "url": "http://google.com",
            "user_id": user.id
        }
    }


@pytest.fixture
def create_invalid_params_missing(user):
    return {
        "bookmark": {
            "title": "Google"
        }
    }


@pytest.fixture
def edit_valid_params():
    return {
        "bookmark": {
            "url": "http://google.com.br"
        }
    }


def test_get_exists(api_test_client, bookmark):
    response = api_test_client.get('/bookmarks/{}'.format(bookmark.id))
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_get_doesnt_exist(api_test_client):
    response = api_test_client.get('/bookmarks/{}'.format(0))
    assert response.status_code == 404


def test_delete_exists(api_test_client, bookmark):
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark.id))
    assert response.status_code == 204


def test_delete_doesnt_exist(api_test_client, bookmark):
    Bookmark.query.filter_by(id=bookmark.id).delete()
    response = api_test_client.delete('/bookmarks/{}'.format(bookmark.id))
    assert response.status_code == 422


def test_post_valid(api_test_client, create_valid_params):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_valid_params),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['bookmark']


def test_post_invalid_params_missing(api_test_client, create_invalid_params_missing):
    response = api_test_client.post('/bookmarks',
                                    data=json.dumps(create_invalid_params_missing),
                                    headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    assert data["errors"]
    assert response.status_code == 422


def test_put_valid(api_test_client, bookmark, edit_valid_params):
    response = api_test_client.put('/bookmarks/{}'.format(bookmark.id),
                                   data=json.dumps(edit_valid_params),
                                   headers={'Content-Type': 'application/json'})
    assert response.status_code == 204
