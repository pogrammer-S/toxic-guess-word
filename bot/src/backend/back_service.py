import requests
from src.config.config import load_config
from urllib.parse import urljoin
from src.database.db_service import return_session
config = load_config()

url = config.API_URL

def start_game(user_id : int):
    try:
        session = return_session(user_id)
        return str(requests.get(url, headers={'user_id': session}).json()["answer_game"])
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"

def answer(user_id : int, message : str):
    try:
        session = return_session(user_id)
        return str(requests.get(urljoin(url, "return_word/"), headers={'user_id': session}, params={"message": message}).json()["answer_game"])
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"

def help(user_id : int):
    try:
        session = return_session(user_id)
        return str(requests.get(urljoin(url, "help/"), headers={'user_id': session}).json()["answer_game"])
    except Exception as e:
        return f"ошибка при выполнении запроса: {e}"