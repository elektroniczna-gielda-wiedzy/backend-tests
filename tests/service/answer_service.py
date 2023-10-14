import requests


class AnswerService:
    def __init__(self, token, app_url):
        self.auth_token = token
        self.app_url = app_url

    def add(self, entry_id, content, image):
        add_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer"
        request_body = {
            "content": content
        }
        if image is not None:
            request_body['image'] = image

        return requests.post(url=add_url, json=request_body, headers={"Authorization": self.auth_token})

    def edit(self, entry_id, answer_id, **kwargs):
        edit_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}"

        return requests.put(url=edit_url, json=kwargs, headers={"Authorization": self.auth_token})

    def delete(self, entry_id, answer_id):
        delete_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}"

        return requests.delete(url=delete_url, headers={"Authorization": self.auth_token})

    def vote(self, entry_id, answer_id, value):
        vote_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}/vote"
        request_body = {
            "value": value
        }
        return requests.put(url=vote_url, json=request_body, headers={"Authorization": self.auth_token})

    def list(self, entry_id):
        list_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer"
        return requests.get(list_url, headers={"Authorization": self.auth_token})

    def top_answer(self, entry_id, answer_id, value):
        top_answer_url = f"{self.app_url}/api/v1/entry/{entry_id}/answer/{answer_id}/top"
        request_body = {
            "value": value
        }
        return requests.put(url=top_answer_url, json=request_body,
                            headers={"Authorization": self.auth_token, "Content-Type": "application/json"})
