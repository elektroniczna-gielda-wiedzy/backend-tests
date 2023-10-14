from ..service.category_service import CategoryService


def test_delete_category_admin(app_url, admin_auth_token):
    # setup
    service = CategoryService(admin_auth_token, app_url)

    # test
    response = service.delete(19)
    category_list = service.list().json()['result']

    # assert
    assert response.ok
    assert not any(
        category['category_id'] == 19 for category in category_list
    )


def test_delete_category_user(app_url, auth_token_user1):
    # setup
    service = CategoryService(auth_token_user1, app_url)

    # test
    response = service.delete(20)
    category_list = service.list().json()['result']

    # assert
    assert not response.ok
    assert any(
        category['category_id'] == 20 for category in category_list
    )
