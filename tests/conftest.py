from os import environ

import pytest

from bookmark_api.app import app as _app
from bookmark_api import db


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
