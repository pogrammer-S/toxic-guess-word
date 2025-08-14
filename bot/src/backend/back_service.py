import requests
from src.config.config import load_config
from urllib.parse import unquote
config = load_config()

url_start = config.API_URL_START
url_post = config.API_URL_POST

def start_game(user_id : int):
    return str(requests.get(url_start+str(user_id)).json()["answer_game"])

def answer(user_id : int, message : str):
    return str(requests.get(url_post+str(user_id)+'/'+unquote(message)).json()["answer_game"])