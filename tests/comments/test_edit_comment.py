from ..service.comment_service import CommentService


def test_edit_comment(auth_token_user1, app_url):
    # setup
    new_content = "a, c = c, a"
    service = CommentService(auth_token_user1, app_url)
    entry_id, answer_id, comment_id = (3, 50, 2)

    # test
    response = service.edit(entry_id, answer_id, comment_id, new_content)
    list_response = service.list(entry_id, answer_id).json()['result']

    # assert
    edited_comment = list(filter(lambda comment: comment['comment_id'] == 2, list_response))[0]
    assert response.ok
    assert edited_comment['content'] == new_content
    assert edited_comment['created_at'] != edited_comment['updated_at']


def test_edit_comment_no_access(auth_token_user1, app_url):
    # setup
    new_content = "a, d = d, a"
    service = CommentService(auth_token_user1, app_url)
    entry_id, answer_id, comment_id = (3, 50, 1)

    # test
    response = service.edit(entry_id, answer_id, comment_id, new_content)
    list_response = service.list(entry_id, answer_id).json()['result']

    # assert
    edited_comment = list(filter(lambda comment: comment['comment_id'] == 1, list_response))[0]
    assert not response.ok
    assert not edited_comment['content'] == new_content
    assert not edited_comment['created_at'] != edited_comment['updated_at']
