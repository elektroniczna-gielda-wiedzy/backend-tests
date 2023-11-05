from ..service.auth_service import AuthService
from ..service.user_service import UserService


def test_success_login(app_url, admin_auth_token):
    # setup
    user_id = 1
    auth_service = AuthService(app_url)
    user_service = UserService(admin_auth_token, app_url)
    user = user_service.get(user_id).json()['result'][0]

    # test
    response = auth_service.login("adamkowalski@student.agh.edu.pl", "L0V3Agh2", True)
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
    login_banned_response = auth_service.login("mariakowalska@student.agh.edu.pl", "L0V3Agh2", True)

    user_unban_response = user_service.unban(2)
    login_unbanned_response = auth_service.login("mariakowalska@student.agh.edu.pl", "L0V3Agh2", True)

    # assert
    assert user_ban_response.ok
    assert not login_banned_response.ok
    assert user_unban_response.ok
    assert login_unbanned_response.ok


def test_reset_password(app_url, auth_token_user3):
    # setup
    auth_service = AuthService(app_url)

    # test
    response = auth_service.reset_password(auth_token_user3, "L0V3Agh2", "newpassword")
    login_response = auth_service.login("marekkrol@student.agh.edu.pl", "newpassword", True)

    # assert
    assert response.ok
    assert login_response.ok

    # cleanup
    auth_service.reset_password(auth_token_user3, "newpassword", "L0V3Agh2")


def test_reset_password_wrong_current(app_url, auth_token_user3):
    # setup
    auth_service = AuthService(app_url)

    # test
    response = auth_service.reset_password(auth_token_user3, "passwordafdasf", "newpassword")
    login_response = auth_service.login("marekkrol@student.agh.edu.pl", "L0V3Agh2", True)

    # assert
    assert not response.ok
    assert login_response.ok
