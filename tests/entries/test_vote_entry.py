from ..service.entries_service import EntriesService


def test_upvote_for_entry(auth_token_user1, auth_token_user2, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)

    # test
    response = service.vote(entry_id, 1)

    # assert
    get_entry_response = service.get(entry_id)
    received_entry = get_entry_response.json()['result'][0]
    assert response.ok
    assert received_entry['user_vote'] == 1
    assert received_entry['votes'] == 1

    # cleanup
    cleanup_entry()


def test_downvote_for_entry(auth_token_user1, auth_token_user2, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)

    # test
    response = service.vote(entry_id, -1)

    # assert
    get_entry_response = service.get(entry_id)
    received_entry = get_entry_response.json()['result'][0]
    assert response.ok
    assert received_entry['user_vote'] == -1
    assert received_entry['votes'] == -1

    # cleanup
    cleanup_entry()


def test_distinct_votes_for_entry(auth_token_user1, auth_token_user2, auth_token_user3, app_url,
                                  create_temporary_entry):
    # setup
    service_user3 = EntriesService(auth_token_user3, app_url)
    service_user1 = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)

    # test
    response_user3 = service_user3.vote(entry_id, 1)
    response_user1 = service_user1.vote(entry_id, -1)

    # assert
    received_entry_user3 = service_user3.get(entry_id).json()['result'][0]
    received_entry_user1 = service_user1.get(entry_id).json()['result'][0]
    assert response_user3.ok
    assert response_user1.ok
    assert received_entry_user3['user_vote'] == 1
    assert received_entry_user1['user_vote'] == -1
    assert received_entry_user3['votes'] == 0
    assert received_entry_user1['votes'] == 0

    # cleanup
    cleanup_entry()


def test_cancel_vote(auth_token_user1, auth_token_user2, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)

    # test
    response = service.vote(entry_id, 1)
    cancel_vote_response = service.vote(entry_id, 0)

    # assert
    received_entry = service.get(entry_id).json()['result'][0]
    assert response.ok
    assert cancel_vote_response.ok
    assert received_entry['user_vote'] == 0

    # cleanup
    cleanup_entry()
