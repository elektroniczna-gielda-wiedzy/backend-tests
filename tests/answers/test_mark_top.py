from ..service.answer_service import AnswerService


def test_mark_top_answer(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    service2 = AnswerService(auth_token_user2, app_url)
    service3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)
    response2 = service2.add(entry_id, "Comment2", None)
    response = service.add(entry_id, "Comment1", None)
    response3 = service3.add(entry_id, "Comment3", None)
    user1_answer_id = response.json()['result'][0]['answer_id']
    response4 = service3.vote(entry_id, user1_answer_id, 1)

    # test
    response5 = service2.top_answer(entry_id, user1_answer_id, 1)

    # assert
    answer_list = service.list(entry_id).json()['result']
    assert response.ok and response2.ok and response3.ok and response4.ok and response5.ok
    assert answer_list[0]['top_answer'] is True
    assert answer_list[1]['top_answer'] is False
    assert answer_list[2]['top_answer'] is False
    assert answer_list[0]['content'] == 'Comment1'


    # cleanup
    cleanup_entry()


def test_mark_top_answer_no_access(auth_token_user1, auth_token_user2,
                                   auth_token_user3, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    service3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)
    response = service3.add(entry_id, "Comment4", None)
    answer_id = response.json()['result'][0]['answer_id']

    # test
    response2 = service.top_answer(entry_id, answer_id, 1)

    # assert
    assert response.ok
    assert not response2.ok

    # cleanup
    cleanup_entry()


def test_mark_own_answer(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)

    # test
    response = service.add(entry_id, "Comment5", None)

    # assert
    answer_id = response.json()['result'][0]['answer_id']
    response2 = service.top_answer(entry_id, answer_id, None)
    assert response.ok
    assert not response2.ok

    # cleanup
    cleanup_entry()


def test_mark_other_answer(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    service2 = AnswerService(auth_token_user2, app_url)
    service3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)
    response2 = service2.add(entry_id, "Comment2", None)
    response = service.add(entry_id, "Comment1", None)
    response3 = service3.add(entry_id, "Comment3", None)
    user1_answer_id = response.json()['result'][0]['answer_id']
    user3_answer_id = response3.json()['result'][0]['answer_id']
    response4 = service3.vote(entry_id, user1_answer_id, 1)
    response5 = service.vote(entry_id, user3_answer_id, 1)

    # test
    response6 = service2.top_answer(entry_id, user1_answer_id, 1)
    answer_list = service.list(entry_id).json()['result']
    response7 = service2.top_answer(entry_id, user3_answer_id, 1)
    answer_list2 = service.list(entry_id).json()['result']

    # assert
    assert (response.ok and response2.ok and response3.ok and
            response4.ok and response5.ok and response6.ok and response7.ok)
    assert answer_list[0]['top_answer'] is True
    assert answer_list[1]['top_answer'] is False
    assert answer_list[2]['top_answer'] is False
    assert answer_list[0]['content'] == 'Comment1'
    # assert answer_list[1]['content'] == 'Comment3' uncomment when sorting is implemented
    # assert answer_list[2]['content'] == 'Comment2'
    assert answer_list2[0]['top_answer'] is True
    assert answer_list2[1]['top_answer'] is False
    assert answer_list2[2]['top_answer'] is False
    assert answer_list2[0]['content'] == 'Comment3'
    # assert answer_list2[1]['content'] == 'Comment1'
    # assert answer_list2[2]['content'] == 'Comment2'

    # cleanup
    cleanup_entry()


def test_unmark_top_answer(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    service2 = AnswerService(auth_token_user2, app_url)
    service3 = AnswerService(auth_token_user3, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)
    response2 = service2.add(entry_id, "Comment2", None)
    response = service.add(entry_id, "Comment1", None)
    response3 = service3.add(entry_id, "Comment3", None)
    user1_answer_id = response.json()['result'][0]['answer_id']
    response4 = service3.vote(entry_id, user1_answer_id, 1)

    # test
    response5 = service2.top_answer(entry_id, user1_answer_id, 1)
    answer_list = service.list(entry_id).json()['result']
    response6 = service2.top_answer(entry_id, user1_answer_id, -1)
    answer_list2 = service.list(entry_id).json()['result']

    # assert
    assert response.ok and response2.ok and response3.ok and response4.ok and response5.ok and response6.ok
    assert answer_list[0]['top_answer'] is True
    assert answer_list[1]['top_answer'] is False
    assert answer_list[2]['top_answer'] is False
    assert answer_list[0]['content'] == 'Comment1'
    assert answer_list2[0]['top_answer'] is False
    assert answer_list2[1]['top_answer'] is False
    assert answer_list2[2]['top_answer'] is False
    # assert answer_list[1]['content'] == 'Comment2' uncomment when sorting is implemented
    # assert answer_list[2]['content'] == 'Comment3'

    # cleanup
    cleanup_entry()
