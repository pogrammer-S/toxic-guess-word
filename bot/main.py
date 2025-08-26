import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

from src.bot.bot import bot
bot.polling(none_stop=True)