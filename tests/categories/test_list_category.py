from ..service.category_service import CategoryService


def test_list_categories(auth_token_user1, app_url):
    # setup
    service = CategoryService(auth_token_user1, app_url)

    # test
    result_list = service.list().json()['result']

    # assert
    expected_example = list(filter(lambda category: category['category_id'] == 9, result_list))[0]
    assert len(result_list) > 0
    assert any(translation['lang_id'] == 1 and translation['name'] == 'Elektrotechnika' for translation in
               expected_example['names'])
    assert any(translation['lang_id'] == 2 and translation['name'] == 'Electrical Engineering' for translation in
               expected_example['names'])
