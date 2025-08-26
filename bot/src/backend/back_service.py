import requests
from urllib.parse import urljoin

class Back_servise():
    def __init__(self, url):
        self.url = url

    def start_game(self):
        try:
            return requests.post(urljoin(self.url, "start/")).json()
        except Exception as e:
            return {"answer_game": f"ошибка при выполнении запроса: {e}"}

    def answer(self, session_id : str, message : str):
        try:
            return requests.post(urljoin(self.url, "guess/"), headers={'X-Session-Id': session_id}, json={'word': message}).json()
        except Exception as e:
            return {"answer_game": f"ошибка при выполнении запроса: {e}"}

    def help(self, session_id : str):
        try:
            return requests.get(urljoin(self.url, "hint/"), headers={'X-Session-Id': session_id}).json()
        except Exception as e:
            return f"ошибка при выполнении запроса: {e}"