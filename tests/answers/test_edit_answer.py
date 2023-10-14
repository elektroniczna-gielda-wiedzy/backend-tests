from ..service.answer_service import AnswerService


def test_edit_answer(auth_token_user1, app_url):
    # setup
    service = AnswerService(auth_token_user1, app_url)
    entry_id, answer_id = (15, 62)
    new_content = "Cześć, chodzi o jakiś dowolny algorytm czy konkretny?"

    # test
    response = service.edit(entry_id, answer_id, content=new_content)

    # assert
    edited_answer = response.json()['result'][0]
    assert edited_answer['content'] == new_content
    assert edited_answer['created_at'] != edited_answer['updated_at']

    # cleanup


def test_edit_answer_no_access(auth_token_user1, auth_token_user2, app_url, create_temporary_answer):
    # setup
    service = AnswerService(auth_token_user2, app_url)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1)
    new_content = "Edited answer"

    # test
    response = service.edit(entry_id, answer_id, content=new_content)

    # assert
    assert not response.ok

    # cleanup
    cleanup_answer()
