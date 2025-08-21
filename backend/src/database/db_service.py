from src.database.connection import cursor
import json
import logging
import uuid

def return_game_state(session_id : str):
    try:
        cursor.execute("SELECT game_state FROM players WHERE session_id = %s", (session_id,))
        return cursor.fetchone()[0]
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")

def insert_game_state(session_id: str, game_state: json):
    try:
        game_state=json.dumps(game_state)

        if not return_game_state(session_id):
            cursor.execute("INSERT INTO players (session_id, game_state) VALUES (%s, %s)", (session_id, game_state,))
            logging.info(f"Записанно {session_id}, {game_state}")
        else:
            cursor.execute("UPDATE players SET game_state = %s WHERE session_id = %s", (game_state, session_id,))
            logging.info(f"Обновленно {session_id}, {game_state}")
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")

def create_session(user_id: str):
    try:
        session_guid = str(uuid.uuid4())
        cursor.execute("INSERT INTO sesion (id, session_guid) VALUES (%s, %s)", (user_id, session_guid,))
        logging.info(f"Записанно {user_id}, {session_guid}")
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")
    

def return_session(user_id: str):
    try:
        logging.info("Возрат сессии")
        cursor.execute("SELECT session_guid FROM sesion WHERE id = %s", (user_id,))
        result = cursor.fetchone()[0]
        if result is None:
            logging.info("Создание сессии")
            create_session(user_id)
            cursor.execute("SELECT session_guid FROM sesion WHERE id = %s", (user_id,))
            return cursor.fetchone()[0]
        return result
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")