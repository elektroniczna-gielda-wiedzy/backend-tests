import pytest

from ..service.answer_service import AnswerService


def test_add_answer_no_image(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    answer_content = "Oczywiście, spójrz na przykład poniżej"
    entry_id, cleanup = create_temporary_entry(auth_token=auth_token_user1)

    # test
    response = service.add(entry_id, answer_content, None)

    # assert
    answer_list = service.list(entry_id).json()['result']
    answer = answer_list[0]
    assert response.ok
    assert len(answer_list) == 1
    assert answer['content'] == answer_content
    assert answer['top_answer'] is False
    assert answer['votes'] == 0

    # cleanup
    cleanup()
    service.delete(entry_id, answer['answer_id'])


@pytest.mark.parametrize("entry_id", [1, 2])
def test_add_answer_to_incorrect_entry_type(auth_token_user1, app_url, entry_id):
    # setup
    service = AnswerService(auth_token_user1, app_url)

    # test
    response = service.add(entry_id, "Świetny wpis", None)

    # assert
    assert not response.ok
