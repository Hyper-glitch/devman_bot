import logging

import telegram

from bot_settings import DEVMAN_TOKEN, TELEGRAM_TOKEN, USERNAME, CHAT_ID
from devman_api import ApiDevMan
from tg_bot import TelegramLogsHandler

logger = logging.getLogger('devman_bot')


def main(telegram_bot):
    logger.info('Bot is running')
    api = ApiDevMan(devman_token=DEVMAN_TOKEN)

    api.get_long_polling(telegram_bot=telegram_bot, username=USERNAME, chat_id=CHAT_ID)


def set_up_logger(telegram_bot, chat_id):
    logger_format = '%(asctime)s %(filename)s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=logger_format)

    tg_handler = TelegramLogsHandler(telegram_bot, chat_id)

    logger.setLevel(logging.INFO)
    logger.addHandler(tg_handler)


if __name__ == '__main__':
    telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)
    set_up_logger(telegram_bot=telegram_bot, chat_id=CHAT_ID)
    main(telegram_bot=telegram_bot)
