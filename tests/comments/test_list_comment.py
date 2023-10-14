from ..service.comment_service import CommentService


def test_list_comments(auth_token_user1, app_url):
    # setup
    service = CommentService(auth_token_user1, app_url)

    # test
    response = service.list(3, 50)

    # assert
    assert response.ok
    assert len(response.json()['result']) == 2
