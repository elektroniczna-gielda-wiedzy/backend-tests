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
