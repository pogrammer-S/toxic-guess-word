import requests
from src.config.config import load_config
from urllib.parse import urljoin
config = load_config()

url = config.API_URL

def start_game(user_id : int):
    try:
        return requests.get(url, headers={'user_id': str(user_id)}).json()
    except Exception as e:
        return {"answer_game": f"ошибка при выполнении запроса: {e}"}

def answer(user_id : int, message : str):
    try:
        return requests.get(urljoin(url, "return_word/"), headers={'user_id': str(user_id)}, params={"message": message}).json()
    except Exception as e:
        return {"answer_game": f"ошибка при выполнении запроса: {e}"}

def help(user_id : int):
    try:
        return requests.get(urljoin(url, "help/"), headers={'user_id': str(user_id)}).json()["answer_game"]
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"