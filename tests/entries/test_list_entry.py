from ..service.entries_service import EntriesService


def test_list_all(auth_token_user1, app_url):
    # setup
    expected_title = "Szukam grupy do nauki termodynamiki"
    service = EntriesService(auth_token_user1, app_url)

    # test
    response = service.list()
    response_list = response.json()['result']

    # assert
    assert response.ok
    assert len(response_list) == 18
    assert any(entry['title'] == expected_title for entry in response_list)


def test_list_sort_by_created(auth_token_user1, app_url, create_temporary_entry):
    # setup
    entry_id, cleanup = create_temporary_entry(auth_token=auth_token_user1)
    service = EntriesService(auth_token_user1, app_url)

    # test
    response = service.list(sort=0)
    response_list = response.json()['result']

    # assert
    assert response.ok
    assert response_list[0]['entry_id'] == entry_id

    # cleanup
    cleanup()


def test_list_sort_by_modified(auth_token_user1, auth_token_user2, app_url, create_temporary_entry):
    # setup
    entry_id, cleanup = create_temporary_entry(auth_token=auth_token_user1)
    entry_id2, cleanup2 = create_temporary_entry(auth_token=auth_token_user2)
    service = EntriesService(auth_token_user1, app_url)

    # test
    service.edit(entry_id, new_title="New title")
    response = service.list(sort=1)
    response_list = response.json()['result']

    # assert
    assert response.ok
    assert response_list[0]['entry_id'] == entry_id
    assert response_list[1]['entry_id'] == entry_id2

    # cleanup
    cleanup()
    cleanup2()

def test_list_sort_by_votes(auth_token_user1, auth_token_user2, auth_token_user3, app_url, create_temporary_entry):
    # setup
    service = EntriesService(auth_token_user1, app_url)
    service2 = EntriesService(auth_token_user2, app_url)
    service3 = EntriesService(auth_token_user3, app_url)

    service.vote(2, 1)
    service.vote(8, -1)
    service2.vote(2, 1)
    service2.vote(8, 1)
    service2.vote(9, -1)
    service3.vote(1, -1)
    service3.vote(8, -1)
    service3.vote(9, -1)
    service3.vote(7, 1)

    # test
    response = service.list(sort=2)
    response_list = response.json()['result']

    # assert
    list_given = list(map(lambda entry: entry['entry_id'], response_list))
    list_expected = list(map(lambda entry: entry['entry_id'], sorted(response_list, key=lambda entry: entry['votes'] ,reverse=True)))

    assert list_given == list_expected

def test_categories_sorted_persistent(auth_token_user1, app_url):
    # setup
    service = EntriesService(auth_token_user1, app_url)

    # test
    prev_list = None
    for i in range(10):
        response = service.list(sort=1)
        response_list = response.json()['result']
        first_entry_cat = response_list[0]['categories']
        current_list = list(map(lambda category: category['category_id'], first_entry_cat))
        if prev_list is not None:
            assert current_list == prev_list
        prev_list = current_list
    # assert
    assert response.ok


