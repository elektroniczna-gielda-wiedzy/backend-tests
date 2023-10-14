from ..service.entries_service import EntriesService


def test_add_entry_no_image(app_url, auth_token_user1):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_title = "Ta notatka opisuje podstawowe struktury danych"
    entry_content = "Podstawowymi strukturami danych możemy nazwać listę, drzewo..."
    entry_categories = [1, 16]
    entry_type_id = 1

    # test
    response = service.add(entry_type_id, entry_title, entry_content, entry_categories, None)

    # assert
    entry_response = response.json()['result'][0]
    assert response.ok
    assert entry_response['title'] == entry_title
    assert entry_response['content'] == entry_content
    assert entry_response['categories'][0]['category_id'] in entry_categories
    assert entry_response['categories'][1]['category_id'] in entry_categories
    assert entry_response['entry_type_id'] == entry_type_id

    # teardown
    cleanup_response = service.delete(entry_response['entry_id'])
    assert cleanup_response.ok
