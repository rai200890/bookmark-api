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
    _app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI_TEST")
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['TESTING'] = True
    _app.config['SECRET_KEY'] = "super-secret"
    recreate_database()


@pytest.fixture(scope="session")
def app(request):
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        request.addfinalizer(teardown)
    return _app


@pytest.fixture(autouse=True)
def rollback(app, request):
    def fin():
        db.session.rollback()
        recreate_database()

    request.addfinalizer(fin)


@pytest.fixture
def api_test_client(app):
    return app.test_client()
