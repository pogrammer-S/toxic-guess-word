from src.config.config import load_config
from telebot.handler_backends import State, StatesGroup
config = load_config()
import logging

from src.backend.back_service import Back_servise
backend_client = Back_servise(config.API_URL)

import telebot
bot = telebot.TeleBot(config.BOT_TOKEN)

logging.info(f"Бот {bot.get_me().username} запущен")

from .handler import load_handlers
from .command import load_command

load_command(bot)
load_handlers(bot)
logging.info("Готов к работе")