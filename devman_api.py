import logging
import time
import urllib.parse as urllib
from typing import List

import requests
import telegram
from dotenv import load_dotenv

from bot_settings import DEVMAN_TOKEN, TELEGRAM_TOKEN, USERNAME, CHAT_ID
from tg_bot import send_notification
from utils import TelegramLogsHandler


class ApiDevMan:
    def __init__(self, devman_token):
        self.base_url = 'https://dvmn.org/api/'
        self.token = devman_token
        self.header = {'Authorization': 'Token ' + self.token}

    def get_user_reviews(self) -> List:
        endpoint = 'user_reviews/'
        user_reviews_url = urllib.urljoin(self.base_url, endpoint)
        response = requests.get(url=user_reviews_url, headers=self.header)
        response.raise_for_status()
        user_reviews = response.json().get('results')
        return user_reviews

    def get_long_polling(self, telegram_bot, username, chat_id):
        endpoint = 'long_polling/'
        long_polling_url = urllib.urljoin(self.base_url, endpoint)
        params = None

        while True:
            try:
                response = requests.get(url=long_polling_url, headers=self.header, timeout=90, params=params, )
                long_polling = response.json()

                status = long_polling.get('status')

                if status == 'timeout':
                    timestamp = long_polling.get('timestamp_to_request')
                    params = {'timestamp': timestamp}
                    continue
                else:
                    timestamp = long_polling.get('last_attempt_timestamp')
                    params = {'timestamp': timestamp}

            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(180)
                continue

            new_attempts = long_polling.get('new_attempts')
            user_review = new_attempts[0]

            lesson_title = user_review.get('lesson_title')
            lesson_url = user_review.get('lesson_url')
            is_lesson_failed = user_review.get('is_negative')

            send_notification(
                username=username, lesson_title=lesson_title, chat_id=chat_id,
                lesson_url=lesson_url, is_lesson_failed=is_lesson_failed, telegram_bot=telegram_bot,
            )


def main():
    logger.info('Bot is running')
    load_dotenv()
    logger_format = '%(asctime)s %(filename)s %(levelname)s %(message)s'

    telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)
    set_up_logger(telegram_bot=telegram_bot, chat_id=CHAT_ID, logger_format=logger_format)
    api = ApiDevMan(devman_token=DEVMAN_TOKEN)

    api.get_long_polling(telegram_bot=telegram_bot, username=USERNAME, chat_id=CHAT_ID)


def set_up_logger(telegram_bot, chat_id, logger_format):
    logging.basicConfig(level=logging.INFO, format=logger_format)

    tg_handler = TelegramLogsHandler(telegram_bot, chat_id)
    logger.setLevel(logging.INFO)
    logger.addHandler(tg_handler)


if __name__ == '__main__':
    logger = logging.getLogger('devman_bot')
    main()
