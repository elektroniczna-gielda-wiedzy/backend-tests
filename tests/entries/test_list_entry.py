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
