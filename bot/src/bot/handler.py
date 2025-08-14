from src.backend.back_service import answer

def load_handlers(bot):
    bot.register_message_handler(handler_message, content_types=['text'])   

from .bot import bot

def handler_message(message):
    bot.send_message(message.chat.id, str(answer(message.from_user.id, message.text)))