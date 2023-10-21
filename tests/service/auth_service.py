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
