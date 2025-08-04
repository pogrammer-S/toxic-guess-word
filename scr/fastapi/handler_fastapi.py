from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from main import game, templates, app, game_state

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def play_game(request: Request):
    return templates.TemplateResponse("game_page.html", {"request": request, "game": game_state})

@router.post("/return_word", response_class=HTMLResponse)
async def return_answer(request: Request, message: str = Form(...)):
    message = message.lower()
    clean_word = game.add_pos_tag(message)

    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": game.checking_word(clean_word, message)
    }

    return templates.TemplateResponse("game_page.html", {"request": request, "game": game_state})