import logging
import os

import telegram
from dotenv import load_dotenv

from devman_api import ApiDevMan
from tg_bot import TelegramLogsHandler


def main():
    logger = logging.getLogger('devman_bot')
    logger_format = '%(asctime)s %(filename)s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=logger_format)
    logger.info('Bot is running')

    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TG_TOKEN')
    username = os.getenv('TG_USERNAME')
    chat_id = os.getenv('TG_CHAT_ID')

    api = ApiDevMan(devman_token=devman_token)
    telegram_bot = telegram.Bot(token=telegram_token)
    telegram_handler = TelegramLogsHandler(telegram_bot, chat_id)
    logger.addHandler(telegram_handler)

    api.get_long_polling(telegram_bot=telegram_bot, username=username, chat_id=chat_id)


if __name__ == '__main__':
    main()
