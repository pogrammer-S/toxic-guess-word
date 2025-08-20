from src.backend.back_service import start_game, help
import ast
import logging

def load_command(bot):
    bot.register_message_handler(command_start, commands=['start'])
    bot.register_message_handler(command_help, commands=['help'])
    logging.info("Команды загруженны")

from .bot import bot

def command_start(message):
    try:
        logging.info("Полученна команда /start")
        answer_server = start_game(message.from_user.id)
        if answer_server == "Старт":
            bot.send_message(message.chat.id, "<b>Введите слово.</b>\nДоступные комманды: /help - для получения подсказки,\n/start - для начала новой игры", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, answer_server)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка команда /start:{e}")

def command_help(message):
    try:
        logging.info("Полученна команда /help")
        answer_server = help(message.from_user.id)
        if "Помощь" in answer_server.split():
            html_list = ast.literal_eval(answer_server[answer_server.find('['):answer_server.rfind(']') + 1])
            bot.send_message(message.chat.id, f"<b>Подсказка:</b>\n{html_list}", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, answer_server)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка команда /help:{e}")