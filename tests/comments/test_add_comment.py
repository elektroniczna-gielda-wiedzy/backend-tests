from ..service.comment_service import CommentService


def test_add_comment(auth_token_user1, auth_token_user2, app_url, create_temporary_entry, create_temporary_answer):
    # setup
    service = CommentService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)
    entry_id, answer_id, cleanup_answer = create_temporary_answer(auth_token=auth_token_user1, entry_id=entry_id)

    # test
    response = service.add(entry_id, answer_id, "Example comment")
    comment_response = service.list(entry_id, answer_id).json()['result']

    # assert
    assert response.ok
    assert len(comment_response) == 1
    assert comment_response[0]['content'] == 'Example comment'

    # cleanup
    cleanup_answer()
    cleanup_entry()
