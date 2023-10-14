from ..service.comment_service import CommentService


def test_delete_comment(auth_token_user1, app_url, create_temporary_comment):
    # setup
    entry_id, answer_id, comment_id, cleanup_comment = create_temporary_comment(auth_token=auth_token_user1)
    service = CommentService(auth_token_user1, app_url)

    # test
    response = service.delete(entry_id, answer_id, comment_id)
    comments = service.list(entry_id, answer_id).json()['result']

    # assert
    assert response.ok
    assert len(comments) == 0


def test_delete_comment_admin(admin_auth_token, auth_token_user2, app_url, create_temporary_comment):
    # setup
    entry_id, answer_id, comment_id, cleanup_comment = create_temporary_comment(auth_token=auth_token_user2)
    service = CommentService(admin_auth_token, app_url)

    # test
    response = service.delete(entry_id, answer_id, comment_id)
    comments = service.list(entry_id, answer_id).json()['result']

    # assert
    assert response.ok
    assert len(comments) == 0


def test_delete_comment_no_access(auth_token_user1, auth_token_user2, app_url, create_temporary_comment):
    # setup
    entry_id, answer_id, comment_id, cleanup_comment = create_temporary_comment(auth_token=auth_token_user1)
    service = CommentService(auth_token_user2, app_url)

    # test
    response = service.delete(entry_id, answer_id, comment_id)
    comments = service.list(entry_id, answer_id).json()['result']

    # assert
    assert not response.ok
    assert len(comments) == 1

    # cleanup
    cleanup_comment()
