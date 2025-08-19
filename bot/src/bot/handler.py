from src.backend.back_service import answer
import ast

def load_handlers(bot):
    bot.register_message_handler(handler_message, content_types=['text'])   

from .bot import bot

def handler_message(message):
    try:
        answer_server = str(answer(message.from_user.id, message.text))
        if answer_server == "Нет слова":
            bot.send_message(message.chat.id, f"<b>Слово <i>{message.text}</i> отсутствует в модели.</b>", parse_mode="HTML")
        elif answer_server == "Только существительные":
            bot.send_message(message.chat.id, "<b>Только существительные</b>", parse_mode="HTML")
        elif "Победа" in answer_server.split():
            tryer = answer_server.split()[1]
            helper = ast.literal_eval(answer_server[answer_server.find('['):answer_server.rfind(']') + 1])
            bot.send_message(message.chat.id, f"<b>Вы победили за {tryer} попыток. Загаданно новое слово</b>\n<i>Подсказка:</i>\n{helper}", parse_mode="HTML")
        elif answer_server == "Было":
            bot.bot.send_message(message.chat.id, "<b>Это слово уже было</b>", parse_mode="HTML")
        elif "Неверно" in answer_server.split():
            dist = answer_server.split()[1]
            bot.send_message(message.chat.id, f"<b>Неправильное слово.</b>\n<i>Расстояние до правильного: {dist}</i>", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, answer_server, parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка:\n<b>{e}</b>", parse_mode="HTML")