from ..service.user_service import UserService
from ..service.entries_service import EntriesService


def test_getting_own_info(auth_token_user1, auth_token_user2, auth_token_user3, app_url):
    # setup
    service = UserService(auth_token_user1, app_url)
    entry_service_user2 = EntriesService(auth_token_user2, app_url)
    entry_service_user3 = EntriesService(auth_token_user3, app_url)
    entry_service_user2.vote(4, 1)
    entry_service_user2.vote(5, 1)
    entry_service_user2.vote(6, -1)
    entry_service_user3.vote(4, 1)
    entry_service_user3.vote(5, 1)
    entry_service_user3.vote(6, 1)

    # test
    response = service.get(1)

    # assert
    user_info = response.json()['result'][0]
    assert response.ok
    assert user_info['email'] == 'adamkowalski@student.agh.edu.pl'
    assert user_info['created_at'] is not None
    assert user_info['last_login'] is not None
    assert user_info['basic_info']['user_id'] == 1
    assert user_info['basic_info']['first_name'] == 'Adam'
    assert user_info['basic_info']['last_name'] == 'Kowalski'
    assert user_info['activity']['no_entries']['Announcement'] == 0
    assert user_info['activity']['no_entries']['Note'] == 2
    assert user_info['activity']['no_entries']['Post'] == 1
    assert user_info['activity']['no_votes']['Announcement']['positive'] == 0
    assert user_info['activity']['no_votes']['Note']['positive'] == 3
    assert user_info['activity']['no_votes']['Post']['positive'] == 2
    assert user_info['activity']['no_votes']['Announcement']['negative'] == 0
    assert user_info['activity']['no_votes']['Note']['negative'] == 1
    assert user_info['activity']['no_votes']['Post']['negative'] == 0


def test_getting_other_user_info(auth_token_user2, app_url):
    # setup
    service = UserService(auth_token_user2, app_url)

    # test
    response = service.get(1)

    # assert
    user_info = response.json()['result'][0]
    assert response.ok
    assert 'email' not in user_info
    assert 'created_at' not in user_info
    assert 'last_login' not in user_info
    assert user_info['basic_info']['user_id'] == 1
    assert user_info['basic_info']['first_name'] == 'Adam'
    assert user_info['basic_info']['last_name'] == 'Kowalski'
    assert 'activity' not in user_info
