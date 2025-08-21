from fastapi import APIRouter, Header
from main import game, model_manager
from src.database.db_service import insert_game_state, return_session
import logging

router = APIRouter()

@router.get("/")
async def play_game(user_id : str = Header(...)):
    game.new_game()
    session_id = return_session(user_id)
    logging.info(f"Юзер:{user_id}, сессия:{session_id}")
    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": "Старт"
    }

    insert_game_state(session_id, game_state)
    game_state.pop("random_word")
    return game_state

@router.get("/return_word/")
async def return_answer(message: str, user_id: str = Header(...)):
    message = message.lower()
    clean_word = model_manager.add_pos_tag(message)
    session_id = return_session(user_id)
    logging.info(f"Юзер:{user_id}, сессия:{session_id}")
    answer=game.checking_word(clean_word, session_id)

    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": answer
    }
    
    insert_game_state(session_id, game_state)
    game_state.pop("random_word")
    return game_state

@router.get("/help/")
async def help(user_id: str = Header(...)):
    session_id = return_session(user_id)
    logging.info(f"Юзер:{user_id}, сессия:{session_id}")
    
    game_state = {
    "random_word": game.random_word,
    "tryers": game.tryers,
    "old_messages": game.old_messages,
    "answer_game": game.help(session_id)
    }
    
    insert_game_state(session_id, game_state)
    game_state.pop("random_word")
    return game_state