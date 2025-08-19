import requests
from src.config.config import load_config
from urllib.parse import urljoin
config = load_config()

url = config.API_URL

def start_game(user_id : int):
    try:
        return str(requests.get(url, params={'user_id': user_id}).json()["answer_game"])
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"

def answer(user_id : int, message : str):
    try:
        return str(requests.get(urljoin(url, "return_word/"), params={'user_id': user_id, "message": message}).json()["answer_game"])
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"

def help(user_id : int):
    try:
        return str(requests.get(urljoin(url, "help/"), params={'user_id': user_id}).json()["answer_game"])
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"