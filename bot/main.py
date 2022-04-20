import logging
import os

import telegram
from dotenv import load_dotenv

from devman_api import ApiDevMan
from tg_bot import TelegramLogsHandler

logger = logging.getLogger('devman_bot')


def main():
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TG_TOKEN')
    username = os.getenv('TG_USERNAME')
    chat_id = os.getenv('TG_CHAT_ID')

    logger_format = '%(asctime)s %(filename)s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=logger_format)
    telegram_bot = telegram.Bot(token=telegram_token)
    telegram_handler = TelegramLogsHandler(telegram_bot, chat_id)
    logger.addHandler(telegram_handler)

    run_telegram_bot(devman_token=devman_token, telegram_bot=telegram_bot, username=username, chat_id=chat_id)


def run_telegram_bot(devman_token, telegram_bot, username, chat_id):
    logger.info('Bot is running')
    api = ApiDevMan(devman_token=devman_token)
    api.get_long_polling(telegram_bot=telegram_bot, username=username, chat_id=chat_id)


if __name__ == '__main__':
    main()
