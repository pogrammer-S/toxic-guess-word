from src.backend.back_service import start_game, help

def load_command(bot):
    bot.register_message_handler(command_start, commands=['start'])
    bot.register_message_handler(command_help, commands=['help'])

from .bot import bot

def command_start(message):
    bot.send_message(message.chat.id, start_game(message.from_user.id))

def command_help(message):
    bot.send_message(message.chat.id, help(message.from_user.id))