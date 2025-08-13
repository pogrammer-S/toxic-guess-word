import telebot
bot = telebot.TeleBot(config.BOT_TOKEN)
from src.config.config import load_config
from .handler import load_handlers
from .command import load_command

config = load_config()

url = config.API_URL


load_handlers(bot)
load_command(bot)