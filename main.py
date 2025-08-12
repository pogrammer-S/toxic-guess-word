from src.config.config import load_config
from src.model.model_manager import ModelManager
from src.model.connect import model
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    

config = load_config()
model_manager=ModelManager()
from src.game.game_class import Game
game = Game()
app = FastAPI()
    
templates = Jinja2Templates(directory="src/fastapi")

game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": "введите сообщение"
}

from src.fastapi.handler_fastapi import router
app.include_router(router)