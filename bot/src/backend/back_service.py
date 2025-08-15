import requests
from src.config.config import load_config
from urllib.parse import unquote
config = load_config()

url_start = config.API_URL_START
url_return_word = config.API_URL_RETURN_WORD
url_help = config.API_URL_HELP

def start_game(user_id : int):
    return str(requests.get(url_start+str(user_id)).json()["answer_game"])

def answer(user_id : int, message : str):
    return str(requests.get(url_return_word+str(user_id)+'/'+unquote(message)).json()["answer_game"])

def help(user_id : int):
    return str(requests.get(url_help+str(user_id)).json()["answer_game"])