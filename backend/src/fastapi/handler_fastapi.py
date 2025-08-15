from fastapi import APIRouter
from main import game, model_manager
from src.database.db_service import insert_game_state

router = APIRouter()

@router.get("/{user_id}")
async def play_game(user_id : int):
    game.new_game()
    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": "Введите слово"
    }
    insert_game_state(user_id, game_state)
    return game_state

@router.get("/return_word/{user_id}/{message}")
async def return_answer(user_id: int, message: str):
    message = message.lower()
    clean_word = model_manager.add_pos_tag(message)

    answer=game.checking_word(clean_word, message, user_id)

    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": answer
    }

    insert_game_state(user_id, game_state)

    return game_state

@router.get("/help/{user_id}")
async def help(user_id: int):

    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": game.help(user_id)
    }

    insert_game_state(user_id, game_state)

    return game_state