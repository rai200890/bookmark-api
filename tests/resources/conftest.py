import json

import pytest

from bookmark_api import db
from bookmark_api.models import User, Role


@pytest.fixture(scope="session")
def admin_credentials():
    return {"username": "admin", "password": "admin"}


@pytest.fixture(scope="session")
def client_credentials():
    return {"username": "client", "password": "client"}


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


@pytest.fixture(scope="function", autouse=True)
def other_client(client_role):
    user = User(username="joe", email="joe@email.com")
    user.hash_password("joe")
    user.role = client_role
    db.session.add(user)
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
