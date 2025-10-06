import requests

class Post:
    def __init__(self):
        self._url = "https://api.npoint.io/c790b4d5cab58020d391"
        self.all_posts = {}

    def get_all_posts(self):
        resp = requests.get(self._url)
        self.all_posts = resp.json()
        return self.all_posts

    def get_post(self, pid: int):
        for post in self.all_posts:
            if post["id"] == pid:
                break
        else:
            post = {}
        return post
