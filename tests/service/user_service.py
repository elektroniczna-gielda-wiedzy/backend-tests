import requests


class UserService:
    def __init__(self, token, app_url):
        self.token = token
        self.app_url = app_url

    def get(self, user_id):
        get_user_url = f"{self.app_url}/api/v1/user/{user_id}"

        return requests.get(url=get_user_url, headers={"Authorization": self.token, "Content-Type": "application/json"})

    def find(self, query):
        find_user_url = f"{self.app_url}/api/v1/user?query={query}"

        return requests.get(url=find_user_url,
                            headers={"Authorization": self.token, "Content-Type": "application/json"})

    def ban(self, user_id):
        ban_user_url = f"{self.app_url}/api/v1/user/{user_id}/ban"
        request_body = {
            "value":1
        }

        return requests.post(url=ban_user_url,
                             json=request_body,
                            headers={"Authorization": self.token, "Content-Type": "application/json"})

    def unban(self, user_id):
        ban_user_url = f"{self.app_url}/api/v1/user/{user_id}/ban"
        request_body = {
            "value": -1
        }

        return requests.post(url=ban_user_url,
                             json=request_body,
                             headers={"Authorization": self.token, "Content-Type": "application/json"})