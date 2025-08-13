from backend.back_service import start_game

def load_command(bot):
    bot.register_message_handler(command_start, commands=['start'])

from .bot import bot

def command_start(message):
    bot.send_message(message.chat.id, start_game(message.from_user.id))