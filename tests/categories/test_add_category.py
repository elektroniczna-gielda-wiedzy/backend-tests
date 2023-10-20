import pytest

from ..service.category_service import CategoryService


@pytest.mark.parametrize("polish_name, english_name, category_type, parent_id, status", [
    ("Informatyka i Systemy Inteligentne", "Computer Science and Intelligent Systems", 0, 2, 0),
    ("Nauki humanistyczne", "Humanities", 1, None, 0)])
def test_add_category_admin(app_url, admin_auth_token, polish_name, english_name, category_type, parent_id, status):
    # setup
    service = CategoryService(admin_auth_token, app_url)
    translations = [{
        "lang_id": 1,
        "name": polish_name
    }, {
        "lang_id": 2,
        "name": english_name
    }]

    # test
    response = service.add(category_type, translations, parent_id, status)
    category_id = response.json()['result'][0]['category_id']
    categories_list = service.list().json()['result']

    # assert
    assert response.ok
    assert any(
        category['category_id'] == category_id and
        category['type'] == category_type and
        category['parent_id'] == parent_id and
        any(category_name['lang_id'] == 1 and category_name['name'] == polish_name for category_name in
            category['names']) and
        any(category_name['lang_id'] == 2 and category_name['name'] == english_name for category_name in
            category['names'])
        for category in categories_list
    )

    # cleanup
    service.delete(category_id)


@pytest.mark.parametrize("polish_name, english_name, category_type, parent_id, status", [
    ("Socjologia2", "Sociology2", 0, 2, 0),
    ("Nauki humanistyczne2", "Humanities2", 1, None, 0)])
def test_add_category_user_no_access(app_url, auth_token_user1, polish_name, english_name, category_type, parent_id,
                                     status):
    # setup
    service = CategoryService(auth_token_user1, app_url)
    translations = [{
        "lang_id": 1,
        "name": polish_name
    }, {
        "lang_id": 2,
        "name": english_name
    }]

    # test
    response = service.add(category_type, translations, parent_id, status)
    categories_list = service.list().json()['result']

    # assert
    assert not response.ok
    assert not any(
        category['type'] == category_type and
        category['parent_id'] == parent_id and
        any(category_name['lang_id'] == 1 and category_name['name'] == polish_name for category_name in
            category['names']) and
        any(category_name['lang_id'] == 2 and category_name['name'] == english_name for category_name in
            category['names'])
        for category in categories_list
    )
