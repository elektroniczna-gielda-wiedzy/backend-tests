from ..service.answer_service import AnswerService


def test_delete_answer(auth_token_user1, app_url, create_temporary_answer):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1)

    # test
    response = service.delete(entry_id, answer_id)
    answers_list = service.list(entry_id).json()['result']

    # assert
    assert response.ok
    assert len(answers_list) == 0


def test_delete_answer_bad_id(auth_token_user1, app_url):
    # setup
    service = AnswerService(auth_token_user1, app_url)

    # test
    response = service.delete(15, 9999)

    # assert
    assert not response.ok


def test_delete_answer_no_access(auth_token_user1, app_url):
    # setup
    service = AnswerService(auth_token_user1, app_url)

    # test
    response = service.delete(3, 51)

    # assert
    assert not response.ok
