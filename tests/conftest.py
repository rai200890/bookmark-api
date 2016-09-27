from os import environ

import pytest

from bookmark_api.app import app as _app
from bookmark_api import db, models


@pytest.fixture(scope='session')
def app(request):
    ctx = _app.app_context()
    ctx.push()

    _app.config['SQLALCHEMY_DATABASE_URI'] = \
        environ.get("SQLALCHEMY_DATABASE_URI_TEST")

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture(scope='session', autouse=True)
def build_db(app):
    db.create_all()
    db.session.commit()


@pytest.fixture(scope='function', autouse=True)
def rollback(app, request):
    def fin():
        db.session.rollback()
    request.addfinalizer(fin)


@pytest.fixture(scope='session')
def api_test_client(app):
    return app.test_client()
