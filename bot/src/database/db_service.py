from src.database.connection import cursor
import logging
import uuid

def create_session(user_id: int):
    try:
        session_guid = str(uuid.uuid4())
        cursor.execute("INSERT INTO sesion (id, session_guid) VALUES (%s, %s)", (user_id, session_guid,))
        logging.info(f"Записанно {user_id}, {session_guid}")
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")
    

def return_session(user_id: int):
    try:
        logging.info("Возрат сессии")
        cursor.execute("SELECT session_guid FROM sesion WHERE id = %s", (user_id,))
        result = cursor.fetchone()[0]
        if result == None:
            logging.info("Создание сессии")
            create_session(user_id)
            cursor.execute("SELECT session_guid FROM sesion WHERE id = %s", (user_id,))
            return cursor.fetchone()[0]
        return result
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса: {e}")