import requests


class AuthService:
    def __init__(self, app_url):
        self.app_url = app_url

    def login(self, email, password, remember_me):
        login_resource = "/api/v1/auth/sign_in"
        request_body = {
            "email": email,
            "password": password,
            "remember_me": remember_me
        }
        return requests.post(url=self.app_url + login_resource, json=request_body)

    def reset_password(self, token, current_password, new_password):
        reset = "/api/v1/auth/reset_password"
        request_body = {
            "old_password": current_password,
            "new_password": new_password
        }
        return requests.put(url=self.app_url + reset, json=request_body, headers={"Authorization": token, "Content-Type": "application/json"})
