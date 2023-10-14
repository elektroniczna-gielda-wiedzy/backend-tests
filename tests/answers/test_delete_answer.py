from ..service.answer_service import AnswerService
from ..service.entries_service import EntriesService


def test_delete_answer(auth_token_user1, app_url, create_temporary_answer):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    entry_service = EntriesService(auth_token_user1, app_url)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1)

    # test
    response = service.delete(entry_id, answer_id)
    answers_list = service.list(entry_id).json()['result']
    entry_answers = entry_service.get(entry_id).json()['result'][0]['answers']

    # assert
    assert response.ok
    assert len(answers_list) == 0
    assert len(entry_answers) == 0


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
