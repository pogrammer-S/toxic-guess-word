from src.database.connection import cursor
import json
import logging

def return_game_state(user_ip : str):
    try:
        cursor.execute("SELECT game_state FROM players WHERE session_id = %s", (user_ip,))
        return cursor.fetchone()[0]
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")

def insert_game_state(user_ip: str, game_state: json):
    try:
        game_state=json.dumps(game_state)

        if not return_game_state(user_ip):
            cursor.execute("INSERT INTO players (session_id, game_state) VALUES (%s, %s)", (user_ip, game_state,))
            logging.info(f"Записанно {user_ip}, {game_state}")
        else:
            cursor.execute("UPDATE players SET game_state = %s WHERE session_id = %s", (game_state, user_ip,))
            logging.info(f"Обновленно {user_ip}, {game_state}")
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")