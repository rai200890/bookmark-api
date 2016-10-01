import pytest


@pytest.fixture
def create_valid_params():
    return {
        "user": {
            "username": "john_doe",
            "email": "john_doe@email.com",
            "password": "unknown",
            "role_id": 2
        }
    }


@pytest.fixture
def create_invalid_params():
    return {
        "user": {
            "username": "john_doe",
            "email": "john_doe@email.com",
        }
    }


@pytest.fixture
def edit_valid_params():
    return {
        "user": {"password": "unknown2"}
    }


@pytest.fixture
def edit_invalid_params():
    return {
        "user": {"email": "raissa@email.com"}
    }
