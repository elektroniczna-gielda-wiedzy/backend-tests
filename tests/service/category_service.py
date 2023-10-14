import requests


class CategoryService:
    def __init__(self, token, app_url):
        self.auth_token = token
        self.app_url = app_url

    def list(self):
        list_url = f"{self.app_url}/api/v1/category"
        return requests.get(url=list_url, headers={"Authorization": self.auth_token})

    def add(self, category_type, names, parent_id, categoryStatus):
        add_url = f"{self.app_url}/api/v1/category"
        request_body = {
            "type": category_type,
            "names": names,
            "parent_id": parent_id,
            "status":categoryStatus
        }
        return requests.post(url=add_url, json=request_body, headers={"Authorization": self.auth_token})

    def update(self, category_id, **kwargs):
        update_url = f"{self.app_url}/api/v1/category/{category_id}"
        return requests.put(url=update_url, json=kwargs, headers={"Authorization": self.auth_token})

    def delete(self, category_id):
        delete_url = f"{self.app_url}/api/v1/category/{category_id}"
        return requests.delete(url=delete_url, headers={"Authorization": self.auth_token})
