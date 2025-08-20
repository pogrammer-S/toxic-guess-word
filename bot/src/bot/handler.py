from src.backend.back_service import answer
import ast
import logging

def load_handlers(bot):
    logging.info("Загрузка хендлера...")
    bot.register_message_handler(handler_message, content_types=['text'])
    logging.info("Хандлер загружен")

from .bot import bot

def handler_message(message):
    try:
        logging.info(f"Полученно сообщение {message}")
        answer_server = answer(message.from_user.id, message.text)
        if answer_server["answer_game"] == "Нет слова":
            bot.send_message(message.chat.id, f"<b>Слово <i>{message.text}</i> отсутствует в модели.</b>", parse_mode="HTML")
        elif answer_server["answer_game"] == "Только существительные":
            bot.send_message(message.chat.id, "<b>Только существительные</b>", parse_mode="HTML")
        elif "Победа" in answer_server["answer_game"].split():
            tryer = answer_server["tryers"]
            helper = ast.literal_eval(answer_server[answer_server.find('['):answer_server["answer_game"].rfind(']') + 1])
            bot.send_message(message.chat.id, f"<b>Вы победили за {tryer} попыток. Загаданно новое слово</b>\n<i>Подсказка:</i>\n{helper}", parse_mode="HTML")
        elif answer_server["answer_game"] == "Было":
            bot.bot.send_message(message.chat.id, "<b>Это слово уже было</b>", parse_mode="HTML")
        elif "Неверно" in answer_server["answer_game"].split():
            dist = answer_server["answer_game"].split()[1]
            bot.send_message(message.chat.id, f"<b>Неправильное слово.</b>\n<i>Расстояние до правильного: {dist}</i>", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, str(answer_server), parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")
        logging.error(f"Ошибка сообщения:{e}")