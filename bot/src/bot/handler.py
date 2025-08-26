import ast
import logging
from src.database.db_services import return_session_id

def load_handlers(bot):
    logging.info("Загрузка хендлера...")
    bot.register_message_handler(handler_message, content_types=['text'])
    logging.info("Хандлер загружен")

from .bot import bot, backend_client

def handler_message(message):
    try:
        logging.info(f"Полученно сообщение {message.text}")
        session_id = return_session_id(message.from_user.id)
        if session_id != None:
            answer_server = backend_client.answer(return_session_id(message.from_user.id), message.text)
            logging.info(f"{str(answer_server)}")
            if answer_server == None:
                bot.send_message(message.chat.id, f"<b>Ошибка запроса</b>", parse_mode="HTML")
                return None
        else:
            bot.send_message(message.chat.id, f"<b>Сессия не найдена</b>", parse_mode="HTML")
            return None

        if answer_server["is_completed"] == True:
            bot.send_message(message.chat.id, f"Вы победили за {answer_server['attempts_left']} попыток\n<b>Игра завершена. Начните новую игру командой</b> /start", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, f"<b>{answer_server['message']}</b>", parse_mode="HTML")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка сообщения:{e}")