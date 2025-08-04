from scr.game.game_class import Game
from scr.model.connect import model
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

game = Game()
app = FastAPI()
templates = Jinja2Templates(directory="scr/fastapi")
game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": "введите сообщение"
}

from scr.fastapi.handler_fastapi import router
app.include_router(router)