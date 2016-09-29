# -*- coding: utf-8 -*-
from os import environ
from datetime import timedelta
import pytest
import json

from bookmark_api.app import app as _app
from bookmark_api import db
from bookmark_api.models import User


def recreate_database():
    try:
        db.drop_all()
        db.create_all()
    except:
        db.session.rollback()


def pytest_sessionstart(session):
    _app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI_TEST"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    recreate_database()


@pytest.fixture(scope='session')
def app(request):
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='function', autouse=True)
def rollback(app, request):
    def fin():
        recreate_database()
    request.addfinalizer(fin)


@pytest.fixture
def admin():
    user = User(username="admin", email="admin@email.com")
    password = "admin"
    user.hash_password(password)
    db.session.add(user)
    db.session.flush()
    return user


@pytest.fixture
def api_test_client(app, mocker, admin):
    test_client = app.test_client()
    mocker.patch("bookmark_api.app.identity", return_value=admin)
    mocker.patch("bookmark_api.app.authenticate", return_value=True)
    return test_client


@pytest.fixture
def admin_auth_headers(api_test_client, admin):
    response = api_test_client.post("/auth",
                                    data=json.dumps({"username": admin.username, "password": "admin"}),
                                    headers={u'content-type': "application/json; charset=utf8"})
    data = json.loads(response.data.decode('utf-8'))
    token = data["access_token"]
    headers = {
        u'content-type': "application/json; charset=utf-8",
        u'authorization': "JWT {}".format(token)
    }
    return headers
