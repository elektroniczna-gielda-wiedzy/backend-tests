import requests
from urllib.parse import urlencode
from ..constants import TIMEOUT_SECONDS

class EntriesService:
    def __init__(self, token, app_url):
        self.token = token
        self.app_url = app_url

    def add(self, entry_type_id, title, content, categories, image):
        add_entry_url = f"{self.app_url}/api/v1/entry"
        request_body = {
            "entry_type_id": entry_type_id,
            "title": title,
            "content": content,
            "categories": categories
        }
        if image is not None:
            request_body['image'] = image

        return requests.post(url=add_entry_url, json=request_body, headers={"Authorization": self.token},
                             timeout=TIMEOUT_SECONDS)

    def edit(self, entry_id, **kwargs):
        edit_entry_url = f"{self.app_url}/api/v1/entry/{entry_id}"
        return requests.put(url=edit_entry_url, json=kwargs, headers={"Authorization": self.token},
                            timeout=TIMEOUT_SECONDS)

    def get(self, entry_id):
        get_entry_url = f"{self.app_url}/api/v1/entry/{entry_id}"
        return requests.get(url=get_entry_url, headers={"Authorization": self.token},
                            timeout=TIMEOUT_SECONDS)

    def list(self, **kwargs):
        list_entries_url = f"{self.app_url}/api/v1/entry?{urlencode(kwargs)}"
        return requests.get(url=list_entries_url, headers={"Authorization": self.token},
                            timeout=TIMEOUT_SECONDS)

    def delete(self, entry_id):
        delete_entry_url = f"{self.app_url}/api/v1/entry/{entry_id}"
        return requests.delete(url=delete_entry_url, headers={"Authorization": self.token},
                               timeout=TIMEOUT_SECONDS)

    def modify_favorites(self, entry_id, favorite):
        favorite_modification_url = f"{self.app_url}/api/v1/entry/{entry_id}/favorite"
        request_body = {"value": favorite}
        return requests.put(url=favorite_modification_url, json=request_body, headers={"Authorization": self.token},
                            timeout=TIMEOUT_SECONDS)

    def vote(self, entry_id, value):
        vote_url = f"{self.app_url}/api/v1/entry/{entry_id}/vote"
        request_body = {"value": value}
        return requests.put(url=vote_url, json=request_body, headers={"Authorization": self.token},
                            timeout=TIMEOUT_SECONDS)
