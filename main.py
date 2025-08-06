from src.game.game_class import Game
from src.model.connect import model
from src.model.model_manager import ModelManager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
from src.config.config import load_config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    
    game = Game()
    model_manager=ModelManager()
    app = FastAPI()
    config = load_config()
    templates = Jinja2Templates(directory="scr/fastapi")
    game_state = {
        "random_word": game.random_word,
        "tryers": game.tryers,
        "old_messages": game.old_messages,
        "answer_game": "введите сообщение"
    }

    from src.fastapi.handler_fastapi import router
    app.include_router(router)