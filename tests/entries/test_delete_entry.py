from ..service.entries_service import EntriesService


def test_delete_entry_with_access(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)

    # test
    response = service.delete(entry_id)

    # assert
    entries_list = service.list().json()['result']
    assert response.ok
    assert not any(entry['entry_id'] == entry_id for entry in entries_list)


def test_delete_entry_no_access(auth_token_user1, auth_token_user2, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)

    # test
    response = service.delete(entry_id)

    # assert
    entries_list = service.list().json()['result']
    assert not response.ok
    assert any(entry['entry_id'] == entry_id for entry in entries_list)

    # cleanup
    cleanup_entry()
