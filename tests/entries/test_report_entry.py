
from tests.service.report_service import ReportService


def test_add_report(app_url, auth_token_user1, admin_auth_token):
    # setup
    topic = "Post o niecodziennym języku"
    description = "Możliwy bot wysyłający posty"
    entry_id = 1
    user_id = 1
    service = ReportService(auth_token_user1, app_url)
    admin_service = ReportService(admin_auth_token, app_url)

    # test
    service.report(topic, description, entry_id)
    response = admin_service.get_reports()
    result_list = response.json()['result'][0]
    result_details = admin_service.get_report(result_list['report_id']).json()['result'][0]
    # assert
    assert response.ok
    assert result_list['report_id'] is not None
    assert result_list['topic'] == topic
    assert result_list['description'] == description
    assert result_details['reporter_id'] == user_id
    assert result_details['entry_id'] == entry_id
    # TODO - check if reporter_id & entry_id not in list
    # TODO - it should be a separate test for adding report and getting report

def test_mark_report_test(app_url, auth_token_user1, admin_auth_token):
    # setup
    topic = "Post o niecodziennym języku2"
    description = "Możliwy bot wysyłający posty2"
    entry_id = 2
    user_id = 1
    service = ReportService(auth_token_user1, app_url)
    admin_service = ReportService(admin_auth_token, app_url)

    # test
    res = service.report(topic, description, entry_id)
    report_id = res.json()['result'][0]['report_id']
    response = admin_service.get_reports().json()['result']
    res2 = admin_service.edit_report(report_id, reviewed=1)
    response2 = admin_service.get_reports().json()['result']

    # assert
    assert res.ok and res2.ok
    assert any(report['report_id'] == report_id for report in response)
    assert not any(report['report_id'] == report_id for report in response2)