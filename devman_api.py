import time
from typing import List
import logging

import requests
import telegram

from bot_settings import DEVMAN_TOKEN, TELEGRAM_TOKEN, USERNAME, CHAT_ID
from tg_bot import send_notification
from utils import TelegramLogsHandler

logger = logging.getLogger('devman_bot')


class ApiDevMan:
    def __init__(self, devman_token):
        self.base_url = 'https://dvmn.org/api/'
        self.token = devman_token
        self.header = {'Authorization': 'Token ' + self.token}

    def get_user_reviews(self) -> List:
        user_reviews_url = self.base_url + 'user_reviews/'
        response = requests.get(url=user_reviews_url, headers=self.header)
        response.raise_for_status()
        user_reviews = response.json().get('results')

        return user_reviews

    def get_long_polling(self, telegram_bot, username, chat_id):
        long_polling_url = self.base_url + 'long_polling/'
        params = None

        while True:
            try:
                response = requests.get(url=long_polling_url, headers=self.header, timeout=90, params=params,)
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

            send_notification(username=username, lesson_title=lesson_title, chat_id=chat_id,
                              lesson_url=lesson_url, is_lesson_failed=is_lesson_failed, telegram_bot=telegram_bot
                              )


def main(telegram_bot):
    logger.info('Bot is running')
    api = ApiDevMan(devman_token=DEVMAN_TOKEN)

    user_reviews = api.get_user_reviews()
    print(user_reviews)
    api.get_long_polling(telegram_bot=telegram_bot, username=USERNAME, chat_id=CHAT_ID)


def set_up_logger(telegram_bot, chat_id):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(filename)s %(levelname)s %(message)s")

    tg_handler = TelegramLogsHandler(telegram_bot, chat_id)
    logger.setLevel(logging.INFO)
    logger.addHandler(tg_handler)


if __name__ == '__main__':
    telegram_bot = telegram.Bot(token=TELEGRAM_TOKEN)

    set_up_logger(telegram_bot=telegram_bot, chat_id=CHAT_ID)
    main(telegram_bot)
