from ..service.user_service import UserService
from ..service.entries_service import EntriesService
from ..constants import *

def test_getting_own_info(auth_token_user1, auth_token_user2, auth_token_user3, app_url):
    service = UserService(auth_token_user1, app_url)
    entry_service_user2 = EntriesService(auth_token_user2, app_url)
    entry_service_user3 = EntriesService(auth_token_user3, app_url)

    entry_service_user2.vote(4, 1)
    entry_service_user2.vote(5, 1)
    entry_service_user2.vote(6, -1)
    entry_service_user3.vote(4, 1)
    entry_service_user3.vote(5, 1)
    entry_service_user3.vote(6, 1)

    response = service.get(1)
    user_info = response.json()['result'][0]

    assert response.ok
    assert user_info['email'] == 'adamkowalski@student.agh.edu.pl'
    assert user_info['created_at'] is not None
    assert user_info['last_login'] is not None
    assert user_info['user_id'] == 1
    assert user_info['first_name'] == 'Adam'
    assert user_info['last_name'] == 'Kowalski'
    assert user_info['entries_count'][ENTRY_ANNOUNCEMENT]['count'] == 0
    assert user_info['entries_count'][ENTRY_NOTE]['count'] == 2
    assert user_info['entries_count'][ENTRY_POST]['count'] == 1
    assert user_info['votes_count'][ENTRY_ANNOUNCEMENT]['positive'] == 0
    assert user_info['votes_count'][ENTRY_NOTE]['positive'] == 3
    assert user_info['votes_count'][ENTRY_POST]['positive'] == 2
    assert user_info['votes_count'][ENTRY_ANNOUNCEMENT]['negative'] == 0
    assert user_info['votes_count'][ENTRY_NOTE]['negative'] == 1
    assert user_info['votes_count'][ENTRY_POST]['negative'] == 0
    assert user_info['is_banned'] is False
    assert user_info['is_email_auth'] is True



def test_getting_other_user_info(auth_token_user2, app_url):
    service = UserService(auth_token_user2, app_url)

    response = service.get(1)
    user_info = response.json()['result'][0]

    assert response.ok
    assert 'email' not in user_info
    assert 'created_at' not in user_info
    assert 'last_login' not in user_info
    assert user_info['user_id'] == 1
    assert user_info['first_name'] == 'Adam'
    assert user_info['last_name'] == 'Kowalski'
    assert 'entries_count' not in user_info
    assert 'voces_count' not in user_info
    #to be discussed
    #assert 'is_banned' not in user_info
    #assert 'is_email_auth' not in user_info


def test_getting_user_info_admin(admin_auth_token, app_url):
    service = UserService(admin_auth_token, app_url)

    response = service.get(9)
    user_info = response.json()['result'][0]

    assert response.ok
    assert user_info['email'] == 'mkowalski@student.agh.edu.pl'
    assert user_info['created_at'] is not None
    assert user_info['last_login'] is not None
    assert user_info['user_id'] == 9
    assert user_info['first_name'] == 'Maciej'
    assert user_info['last_name'] == 'Kowalski'
    assert user_info['entries_count'][ENTRY_NOTE]['count'] == 0
    assert user_info['entries_count'][ENTRY_POST]['count'] == 0
    assert user_info['entries_count'][ENTRY_ANNOUNCEMENT]['count'] == 0
    assert user_info['votes_count'][ENTRY_NOTE]['positive'] == 0
    assert user_info['votes_count'][ENTRY_POST]['positive'] == 0
    assert user_info['votes_count'][ENTRY_ANNOUNCEMENT]['positive'] == 0
    assert user_info['votes_count'][ENTRY_NOTE]['negative'] == 0
    assert user_info['votes_count'][ENTRY_POST]['negative'] == 0
    assert user_info['votes_count'][ENTRY_ANNOUNCEMENT]['negative'] == 0
    assert user_info['is_banned'] is False
    assert user_info['is_email_auth'] is True


