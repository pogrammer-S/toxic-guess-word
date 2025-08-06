from scr.database.connection import cursor
import json

def return_game_state(user_ip : str):
    cursor.execute("SELECT game_state FROM players WHERE ip = %s", (user_ip,))
    return cursor.fetchone()[0]

def insert_game_state(user_ip: str, game_state: json):
    game_state=json.dumps(game_state)

    if not return_game_state(user_ip):
        cursor.execute("INSERT INTO players (ip, game_state) VALUES (%s, %s)", (user_ip, game_state,))
    else:
        cursor.execute("UPDATE players SET game_state = %s WHERE ip = %s", (game_state, user_ip,))