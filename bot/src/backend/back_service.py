import requests
from src.config.config import load_config
config = load_config()

url_start = config.API_URL_START
url_post = config.API_URL_POST

def start_game(user_id : int):
    return requests.get(url_start+str(user_id)).json()

def answer(user_id : int, message):
    return requests.post(url_post+str(user_id), json=message).json()