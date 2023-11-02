import requests


class ReportService:
    def __init__(self, token, app_url):
        self.token = token
        self.app_url = app_url

    def report(self, topic, description, entry_id):
        add_report_url = f"{self.app_url}/api/v1/report"
        request_body = {
            "entry_id": entry_id,
            "topic": topic,
            "description": description
        }

        return requests.post(url=add_report_url,
                             json=request_body,
                             headers={"Authorization": self.token, "Content-Type": "application/json"})

    def get_reports(self):
        get_report_url = f"{self.app_url}/api/v1/report"

        return requests.get(url=get_report_url,
                            headers={"Authorization": self.token, "Content-Type": "application/json"})

    def get_report(self, report_id):
        get_report_url = f"{self.app_url}/api/v1/report/{report_id}"

        return requests.get(url=get_report_url,
                            headers={"Authorization": self.token, "Content-Type": "application/json"})

    def edit_report(self, report_id, **kwargs):
        edit_entry_url = f"{self.app_url}/api/v1/report/{report_id}"

        return requests.put(url=edit_entry_url, json=kwargs, headers={"Authorization": self.token, "Content-Type": "application/json"})
