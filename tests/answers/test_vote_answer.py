from ..service.answer_service import AnswerService


def test_upvotes(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry,
                 create_temporary_answer):
    # setup
    service_user2 = AnswerService(auth_token_user2, app_url)
    service_user3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1, entry_id=entry_id)

    # test
    response1 = service_user2.vote(entry_id, answer_id, 1)
    response2 = service_user3.vote(entry_id, answer_id, 1)
    answer_with_votes = service_user2.list(entry_id).json()['result'][0]

    # assert
    assert response1.ok
    assert response2.ok
    assert answer_with_votes['votes'] == 2

    # cleanup
    cleanup_answer()
    cleanup_entry()


def test_downvotes(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry,
                   create_temporary_answer):
    # setup
    service_user2 = AnswerService(auth_token_user2, app_url)
    service_user3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1, entry_id=entry_id)

    # test
    response1 = service_user2.vote(entry_id, answer_id, -1)
    response2 = service_user3.vote(entry_id, answer_id, -1)
    answer_with_votes = service_user2.list(entry_id).json()['result'][0]

    # assert
    assert response1.ok
    assert response2.ok
    assert answer_with_votes['votes'] == -2

    # cleanup
    cleanup_answer()
    cleanup_entry()


def test_distinct_votes(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry,
                        create_temporary_answer):
    # setup
    service_user2 = AnswerService(auth_token_user2, app_url)
    service_user3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1, entry_id=entry_id)

    # test
    response1 = service_user2.vote(entry_id, answer_id, 1)
    response2 = service_user3.vote(entry_id, answer_id, -1)
    answer_with_votes_user2 = service_user2.list(entry_id).json()['result'][0]
    answer_with_votes_user3 = service_user3.list(entry_id).json()['result'][0]

    # assert
    assert response1.ok
    assert response2.ok
    assert answer_with_votes_user2['votes'] == 0
    assert answer_with_votes_user3['votes'] == 0
    assert answer_with_votes_user2['user_vote'] == 1
    assert answer_with_votes_user3['user_vote'] == -1

    # cleanup
    cleanup_answer()
    cleanup_entry()


def test_votes_limit(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry,
                     create_temporary_answer):
    # setup
    service_user2 = AnswerService(auth_token_user2, app_url)
    service_user3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1, entry_id=entry_id)

    # test
    response1 = service_user2.vote(entry_id, answer_id, -1)
    service_user2.vote(entry_id, answer_id, -1)
    response2 = service_user3.vote(entry_id, answer_id, -1)
    service_user3.vote(entry_id, answer_id, -2)
    answer_with_votes = service_user2.list(entry_id).json()['result'][0]

    # assert
    assert response1.ok
    assert response2.ok
    assert answer_with_votes['votes'] == -2

    # cleanup
    cleanup_answer()
    cleanup_entry()
