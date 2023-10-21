from ..service.answer_service import AnswerService


def test_list_answers(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    entry_id, cleanup = create_temporary_entry(auth_token=auth_token_user1)

    # test
    service.add(entry_id, "Comment 1", None)
    service.add(entry_id, "Comment 2", None)
    service.add(entry_id, "Comment 3", None)

    # assert
    response = service.list(entry_id)
    response_list = response.json()['result']
    assert len(response_list) == 3
    assert any(answer['content'] == 'Comment 1' for answer in response_list)

    # cleanup
    cleanup()


def test_answer_default_sorting(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry):
    # setup
    entry_id, cleanup = create_temporary_entry(auth_token=auth_token_user1)
    service = AnswerService(auth_token_user1, app_url)
    service2 = AnswerService(auth_token_user2, app_url)
    service3 = AnswerService(auth_token_user3, app_url)

    # test
    service.add(entry_id, "test content 1", None)
    service2.add(entry_id, "test content 2", None)
    service3.add(entry_id, "test content 3", None)
    answers = service.list(entry_id).json()['result']

    # assert
    assert answers[0]['content'] == 'test content 1'
    assert answers[1]['content'] == 'test content 2'
    assert answers[2]['content'] == 'test content 3'

    # cleanup
    cleanup()


