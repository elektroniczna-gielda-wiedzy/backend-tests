import requests
from ..constants import TIMEOUT_SECONDS

class CommentService:
    def __init__(self, token, app_url):
        self.auth_token = token
        self.app_url = app_url

    def add(self, entry_id, answer_id, content):
        add_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}/comment"
        request_body = {
            "content": content
        }
        return requests.post(url=add_url, json=request_body, headers={"Authorization": self.auth_token},
                             timeout=TIMEOUT_SECONDS)

    def edit(self, entry_id, answer_id, comment_id, content):
        edit_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}/comment/{comment_id}"
        request_body = {
            "content": content
        }
        return requests.put(url=edit_url, json=request_body, headers={"Authorization": self.auth_token},
                            timeout=TIMEOUT_SECONDS)

    def delete(self, entry_id, answer_id, comment_id):
        delete_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}/comment/{comment_id}"
        return requests.delete(url=delete_url,
                               headers={"Authorization": self.auth_token, "Content-Type": "application/json"},
                               timeout=TIMEOUT_SECONDS)

    def list(self, entry_id, answer_id):
        list_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}/comment"
        return requests.get(url=list_url, headers={"Authorization": self.auth_token},
                            timeout=TIMEOUT_SECONDS)
