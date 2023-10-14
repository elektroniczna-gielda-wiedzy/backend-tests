from ..service.entries_service import EntriesService


def test_add_to_favorites(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)

    # test
    service.modify_favorites(entry_id, 1)

    # assert
    response_list = service.list(favorites=True).json()
    assert any(entry['entry_id'] == entry_id for entry in response_list['result'])

    # cleanup
    cleanup_entry()


def test_remove_from_favorites(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)

    # test
    service.modify_favorites(entry_id, 1)
    service.modify_favorites(entry_id, -1)

    # assert
    response_list = service.list(favorites=True).json()
    assert not any(entry['entry_id'] == entry_id for entry in response_list['result'])

    # cleanup
    cleanup_entry()
