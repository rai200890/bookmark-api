import json
from bookmark_api import db
from bookmark_api.models import User


def setup_module():
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("farofa")
    db.session.add(user)
    db.session.flush()


def test_user_list_get(api_test_client, auth_headers):
    response = api_test_client.get('/users', headers=auth_headers)
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert len(data['users']) == 2
