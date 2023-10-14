from ..service.entries_service import EntriesService


def test_view_entry(auth_token_user1, app_url):
    # setup
    service = EntriesService(auth_token_user1, app_url)

    # test
    response = service.get(3)

    # assert
    response_list = response.json()['result']
    assert response.ok
    assert len(response_list) == 1
    assert response_list[0]['entry_id'] == 3
