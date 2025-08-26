from .connect import cursor
import logging

def check_session(user_id: int):
    cursor.execute("SELECT session_guid FROM sessions_user WHERE user_id = %s", (user_id,))
    answer_bd = cursor.fetchone()
    
    if answer_bd == None:
        return True
    return False

def save_session_id(session_id: str, user_id: int):
        logging.info(f"{user_id}, {session_id}")
        try:
            if check_session(user_id):
                cursor.execute("INSERT INTO sessions_user (user_id, session_guid) VALUES (%s, %s)", (user_id, session_id, ))
                logging.info(f"Созданна новая сессия {user_id}: {session_id}")
            else:
                cursor.execute("UPDATE sessions_user SET session_guid = %s WHERE user_id = %s", (session_id, user_id, ))
                logging.info(f"Обновленна сессия сессия {user_id}: {session_id}")
        except Exception as e:
            logging.error(f"Ошибка сохранения сессии: {e}")

def return_session_id(user_id: int):
    cursor.execute("SELECT session_guid FROM sessions_user WHERE user_id = %s", (user_id,))
    answer_bd = cursor.fetchone()
    logging.info(f"{answer_bd}")
    if not check_session(user_id):
        return answer_bd[0]