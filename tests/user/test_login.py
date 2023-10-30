from ..service.auth_service import AuthService
from ..service.user_service import UserService


def test_success_login(app_url, admin_auth_token):
    # setup
    user_id = 1
    auth_service = AuthService(app_url)
    user_service = UserService(admin_auth_token, app_url)
    user = user_service.get(user_id).json()['result'][0]

    # test
    response = auth_service.login("adamkowalski@student.agh.edu.pl", "password", True)
    user_second_response = user_service.get(user_id).json()['result'][0]

    # assert
    assert response.ok
    assert user['last_login'] != user_second_response['last_login']


def test_bad_login(app_url, admin_auth_token):
    # setup
    user_id = 2
    auth_service = AuthService(app_url)
    user_service = UserService(admin_auth_token, app_url)
    user = user_service.get(user_id).json()['result'][0]

    # test
    response = auth_service.login("mariakowalska@student.agh.edu.pl", "wrongpassword", True)
    user_second_response = user_service.get(user_id).json()['result'][0]

    # assert
    assert not response.ok
    assert user['last_login'] == user_second_response['last_login']

def test_login_banned(app_url, admin_auth_token):
    # setup
    user_id = 2
    auth_service = AuthService(app_url)
    user_service = UserService(admin_auth_token, app_url)

    # test
    user_ban_response = user_service.ban(2)
    login_banned_response = auth_service.login("mariakowalska@student.agh.edu.pl", "password", True)

    user_unban_response = user_service.unban(2)
    login_unbanned_response = auth_service.login("mariakowalska@student.agh.edu.pl", "password", True)

    # assert
    assert user_ban_response.ok
    assert not login_banned_response.ok
    assert user_unban_response.ok
    assert login_unbanned_response.ok