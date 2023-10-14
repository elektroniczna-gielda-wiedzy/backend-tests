from ..service.category_service import CategoryService


def test_edit_category_admin(admin_auth_token, app_url):
    # setup
    service = CategoryService(admin_auth_token, app_url)
    modified_names = [{
        "lang_id": 1,
        "name": "Informatyka Społeczna"
    }, {
        "lang_id": 2,
        "name": "Social Informatics"
    }]

    # test
    update_response = service.update(11, names=modified_names)
    list_response = service.list().json()['result']

    # assert
    modified_category = list(filter(lambda category: category['category_id'] == 11, list_response))[0]
    assert update_response.ok
    assert any(category['lang_id'] == 1 and category['name'] == 'Informatyka Społeczna' for category in
               modified_category['names'])
    assert any(category['lang_id'] == 2 and category['name'] == 'Social Informatics' for category in
               modified_category['names'])


def test_edit_category_user(auth_token_user1, app_url):
    # setup
    service = CategoryService(auth_token_user1, app_url)
    modified_names = [{
        "lang_id": 1,
        "name": "Informatyka Społeczna"
    }, {
        "lang_id": 2,
        "name": "Social Informatics"
    }]

    # test
    update_response = service.update(10, names=modified_names)
    list_response = service.list().json()['result']

    # assert
    modified_category = list(filter(lambda category: category['category_id'] == 10, list_response))[0]
    assert not update_response.ok
    assert not any(category['lang_id'] == 1 and category['name'] == 'Informatyka Społeczna' for category in
                   modified_category['names'])
    assert not any(category['lang_id'] == 2 and category['name'] == 'Social Informatics' for category in
                   modified_category['names'])
