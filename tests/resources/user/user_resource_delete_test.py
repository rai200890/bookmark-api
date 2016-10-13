from bookmark_api.models import User


def test_delete_exists_admin(session, api_test_client, admin_auth_headers, client_role):
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("aaaa")
    user.role = client_role
    session.add(user)
    session.flush()
    
    response = api_test_client.delete('/users/{}'.format(user.id), headers=admin_auth_headers)
    assert response.status_code == 204


def test_delete_exists_other_client(session, api_test_client, client_auth_headers, client_role):
    user = User(username="raissa", email="raissa@email.com")
    user.hash_password("aaaa")
    user.role = client_role
    session.add(user)
    session.flush()

    response = api_test_client.delete('/users/{}'.format(user.id), headers=client_auth_headers)
    assert response.status_code == 403


def test_delete_doesnt_exist(api_test_client, admin_auth_headers):
    response = api_test_client.delete('/users/{}'.format(0), headers=admin_auth_headers)
    assert response.status_code == 403
