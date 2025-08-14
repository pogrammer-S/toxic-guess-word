from src.config.config import load_config
config = load_config()

import telebot
bot = telebot.TeleBot(config.BOT_TOKEN)

from .handler import load_handlers
from .command import load_command

load_command(bot)
load_handlers(bot)