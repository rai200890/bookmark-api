import json

import pytest

from bookmark_api.models import User, Role


@pytest.fixture(scope="session")
def admin_credentials():
    return {"username": "admin", "password": "admin"}


@pytest.fixture(scope="session")
def client_credentials():
    return {"username": "client", "password": "client"}


@pytest.fixture(scope="function")
def admin_role(session):
    role = Role.query.filter_by(name="admin").first()
    if role is None:
        role = Role(name="admin")
        session.add(role)
        session.flush()
    return role


@pytest.fixture(scope="function")
def client_role(session):
    role = Role.query.filter_by(name="client").first()
    if role is None:
        role = Role(name="client")
        session.add(role)
        session.flush()
    return role


@pytest.fixture(scope="function", autouse=True)
def admin(session, admin_credentials, admin_role):
    user = User.query.filter_by(username=admin_credentials["username"]).first()
    if user is None:
        user = User(username=admin_credentials["username"], email="admin@email.com")
        user.hash_password(admin_credentials["password"])
        user.role = admin_role
        session.add(user)
    return user


@pytest.fixture(scope="function", autouse=True)
def client(session, client_credentials, client_role):
    user = User.query.filter_by(username=client_credentials["username"]).first()
    if user is None:
        user = User(username=client_credentials["username"], email="client@email.com")
        user.hash_password(client_credentials["password"])
        user.role = client_role
        session.add(user)
    return user


@pytest.fixture(scope="function")
def other_client(session, client_role):
    user = User(username="joe", email="joe@email.com")
    user.hash_password("joe")
    user.role = client_role
    session.add(user)
    return user


@pytest.fixture
def client_auth_headers(api_test_client, client_credentials):
    response = api_test_client.post("/auth",
                                    data=json.dumps({"username": client_credentials["username"],
                                                    "password": client_credentials["password"]}),
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
                                    data=json.dumps({"username": admin_credentials["username"],
                                                    "password": admin_credentials["password"]}),
                                    headers={"content-type": "application/json; charset=utf8"})
    data = json.loads(response.data.decode("utf-8"))
    token = data["access_token"]
    headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": "JWT {}".format(token)
    }
    return headers
