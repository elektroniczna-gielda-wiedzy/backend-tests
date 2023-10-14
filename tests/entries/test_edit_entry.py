from ..service.entries_service import EntriesService


def test_edit_title_of_entry(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    new_title = "Najistotniejsze zagadnienia z zakresu cyberbezpieczeństwa"
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)

    # test
    response = service.edit(entry_id, title=new_title)

    # assert
    edited_entry = service.get(entry_id)
    assert response.ok
    assert edited_entry.json()['result'][0]['title'] == new_title

    # cleanup
    cleanup_entry()


def test_edit_content_of_entry(auth_token_user1, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user1)
    new_content = ("Ta notatka omówi niektóre z najważniejszych "
                   "zasad cyberbezpieczeństwa, które mogą być użyte do ochrony Twoich informacji. Dowiesz się jak "
                   "stosować najlepsze praktyki z zakresu haseł, bezpiecznych nawyków przeglądania, dwuskładnikowego "
                   "uwierzytelniania, i więcej. Zajrzyj pod poniższy link")

    # test
    response = service.edit(entry_id, content=new_content)

    # assert
    edited_entry = service.get(entry_id)
    assert response.ok
    assert edited_entry.json()['result'][0]['content'] == new_content

    # cleanup
    cleanup_entry()


def test_entry_edit_no_access(auth_token_user1, auth_token_user2, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    new_title = "Najistotniejsze zagadnienia z zakresu cyberbezpieczeństwa"
    entry_id, cleanup_entry = create_temporary_entry(auth_token=auth_token_user2)

    # test
    response = service.edit(entry_id, title=new_title)

    # assert
    edited_entry = service.get(entry_id)
    assert not response.ok
    assert edited_entry.json()['result'][0]['title'] != new_title

    # cleanup
    cleanup_entry()
