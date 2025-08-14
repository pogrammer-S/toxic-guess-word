from src.database.connection import cursor
import json
import logging

def return_game_state(user_ip : str):
    try:
        cursor.execute("SELECT game_state FROM players WHERE id = %s", (user_ip,))
        return cursor.fetchone()[0]
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")

def insert_game_state(user_ip: str, game_state: json):
    try:
        game_state=json.dumps(game_state)

        if not return_game_state(user_ip):
            cursor.execute("INSERT INTO players (id, game_state) VALUES (%s, %s)", (user_ip, game_state,))
            print(f"Записанно {user_ip}, {game_state}")
        else:
            cursor.execute("UPDATE players SET game_state = %s WHERE id = %s", (game_state, user_ip,))
            print(f"Обновленно {user_ip}, {game_state}")
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")