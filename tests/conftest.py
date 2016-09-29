from os import environ

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
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_VERIFY=False,
        JWT_VERIFY_EXPIRATION=False
    )
    recreate_database()


@pytest.fixture(scope='session')
def app(request):
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='function', autouse=True)
def rollback(app, request):
    def fin():
        recreate_database()
    request.addfinalizer(fin)


@pytest.fixture(scope='session')
def api_test_client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def auth_headers(api_test_client):
    user = User(username="admin", email="admin@email.com")
    password = "admin"
    user.hash_password(password)
    db.session.add(user)
    response = api_test_client.post("/auth",
                                    data=json.dumps({"username": user.username, "password": password}),
                                    headers={"Content-Type": "application/json"})
    data = json.loads(response.data.decode('utf-8'))
    return {
        "Content-Type": "application/json",
        "Authorization": "JWT {}".format(data["access_token"])
    }
