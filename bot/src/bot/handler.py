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
        else:
            bot.send_message(message.chat.id, f"<b>Сессия не найдена</b>", parse_mode="HTML")
            return None
        if answer_server["message"] == "Нет слова":
            bot.send_message(message.chat.id, f"<b>Слово <i>{message.text}</i> отсутствует в модели.</b>", parse_mode="HTML")
        elif answer_server["message"] == "Только существительные":
            bot.send_message(message.chat.id, "<b>Только существительные</b>", parse_mode="HTML")
        elif "Победа" in answer_server["message"].split():
            tryer = answer_server["tryers"]
            helper = ast.literal_eval(answer_server[answer_server.find('['):answer_server["message"].rfind(']') + 1])
            bot.send_message(message.chat.id, f"<b>Вы победили за {tryer} попыток. Загаданно новое слово</b>\n<i>Подсказка:</i>\n{helper}", parse_mode="HTML")
        elif answer_server["message"] == "Было":
            bot.bot.send_message(message.chat.id, "<b>Это слово уже было</b>", parse_mode="HTML")
        elif "Неверно" in answer_server["message"].split():
            dist = answer_server["message"].split()[1]
            bot.send_message(message.chat.id, f"<b>Неправильное слово.</b>\n<i>Расстояние до правильного: {dist}</i>", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, answer_server["message"], parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка сообщения:{e}")