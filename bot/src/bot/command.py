import ast
import logging
from src.database.db_services import save_session_id, return_session_id

def load_command(bot):
    logging.info("Загрузка команд...")
    bot.register_message_handler(command_start, commands=['start'])
    bot.register_message_handler(command_help, commands=['help'])
    logging.info("Команды загруженны")

from .bot import bot, backend_client

def command_start(message):
    try:
        logging.info("Полученна команда /start")
        answer_server = backend_client.start_game()
        logging.info(f"Юзер: {message.from_user.id}, сессия: {answer_server["session_id"]}")
        save_session_id(answer_server["session_id"], message.from_user.id)
        bot.send_message(message.from_user.id, f"<b>{answer_server['message']}</b>", parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка команда /start:{e}")

def command_help(message):
    try:
        logging.info("Полученна команда /help")
        answer_server = backend_client.help(return_session_id(message.from_user.id))
        logging.info(f"{answer_server}")
        if len(answer_server['previous_words']) == 0:
            bot.send_message(message.from_user.id, f"<b>Для подсказки необходимо ввести любое слово</b>", parse_mode="HTML")
        else:
            bot.send_message(message.from_user.id, f"<b>Слово межу вашим и правильным:</b>\n{str(get_min_distanse(answer_server))}", parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка команда /help:{e}")


def get_min_distanse(answer_server):
    min_distance_word = min(answer_server["previous_words"], key=lambda x: x["distance"])["word"]
    return min_distance_word