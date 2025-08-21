import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
from src.config.config import load_config
from src.model.model_manager import ModelManager
from src.model.connect import model
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

    

config = load_config()
model_manager=ModelManager()
from src.game.game_class import Game
game = Game()
app = FastAPI()

game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": "введите сообщение"
}

from src.fastapi.handler_fastapi import router
app.include_router(router)