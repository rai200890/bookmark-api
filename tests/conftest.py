from os import environ
import pytest
import json

from bookmark_api.app import app as _app
from bookmark_api import db
from bookmark_api.models import User, Role


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
        recreate_database()

    request.addfinalizer(fin)


@pytest.fixture(scope="session")
def admin_credentials():
    return {"username":"admin", "password": "admin"}


@pytest.fixture(scope="session")
def client_credentials():
    return {"username":"client", "password": "client"}


@pytest.fixture(scope="function", autouse=True)
def admin_role():
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    return role


@pytest.fixture(scope="function", autouse=True)
def client_role():
    role = Role(name="client")
    db.session.add(role)
    db.session.commit()
    return role


@pytest.fixture(scope="function", autouse=True)
def admin(admin_credentials, admin_role):
    user = User(username=admin_credentials["username"], email="admin@email.com")
    user.hash_password(admin_credentials["password"])
    user.role = admin_role
    db.session.add(user)
    return user


@pytest.fixture(scope="function", autouse=True)
def client(client_credentials, client_role):
    user = User(username=client_credentials["username"], email="client@email.com")
    user.hash_password(client_credentials["password"])
    user.role = client_role
    db.session.add(user)
    return user


@pytest.fixture
def api_test_client(app):
    return app.test_client()


@pytest.fixture
def client_auth_headers(api_test_client, client_credentials):
    response = api_test_client.post("/auth",
                                data=json.dumps({"username": client_credentials["username"], "password": client_credentials["password"]}),
                                headers={"content-type": "application/json; charset=utf8"})
    data = json.loads(response.data.decode("utf-8"))
    token = data["access_token"]
    headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": "JWT {}".format(token)
    }
    return headers


@pytest.fixture
def admin_auth_headers(api_test_client, admin_credentials):
    response = api_test_client.post("/auth",
                            data=json.dumps({"username": admin_credentials["username"], "password": admin_credentials["password"]}),
                            headers={"content-type": "application/json; charset=utf8"})
    data = json.loads(response.data.decode("utf-8"))
    token = data["access_token"]
    headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": "JWT {}".format(token)
    }
    return headers
