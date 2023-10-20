from ..service.user_service import UserService


def test_getting_own_info(auth_token_user2, app_url):
    # setup
    service = UserService(auth_token_user2, app_url)

    # test
    response = service.find("Adam Ko")
    response2 = service.find("kowalska ma")

    # assert
    user1 = response.json()['result'][0]
    user2 = response2.json()['result'][0]
    assert response.ok
    assert response2.ok
    assert len(response.json()['result']) == 1
    assert user1['user_id'] == 1
    assert user1['first_name'] == 'Adam'
    assert user1['last_name'] == 'Kowalski'
    assert len(response2.json()['result']) == 1
    assert user2['user_id'] == 2
    assert user2['first_name'] == 'Maria'
    assert user2['last_name'] == 'Kowalska'