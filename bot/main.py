from src.bot.bot import bot
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
bot.polling(none_stop=True)