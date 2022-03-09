import json
import os
import time
from typing import List

import requests
import telegram

from tg_bot import send_notification


class ApiDevMan:
    def __init__(self, devman_token):
        self.base_url = 'https://dvmn.org/api/'
        self.token = devman_token
        self.header = {'Authorization': 'Token ' + self.token}

    def get_user_reviews(self) -> List:
        user_reviews_url = self.base_url + 'user_reviews/'
        user_reviews_response = requests.get(url=user_reviews_url, headers=self.header)
        user_reviews_response.raise_for_status()

        user_reviews_text = json.loads(user_reviews_response.text)
        user_reviews = user_reviews_text.get('results')

        return user_reviews

    def get_long_polling(self, telegram_bot, username, chat_id):
        long_polling_url = self.base_url + 'long_polling/'
        params = None

        while True:
            try:
                long_polling_response = requests.get(url=long_polling_url, headers=self.header,
                                                     timeout=90, params=params,
                                                     )
                long_polling_text = json.loads(long_polling_response.text)

                status = long_polling_text.get('status')

                if status == 'timeout':
                    timestamp = long_polling_text.get('timestamp_to_request')
                    params = {'timestamp': timestamp}
                    continue
                else:
                    timestamp = long_polling_text.get('last_attempt_timestamp')
                    params = {'timestamp': timestamp}

            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                time.sleep(180)
                continue

            long_polling_text = json.loads(long_polling_response.text)
            new_attempts = long_polling_text.get('new_attempts')
            user_review = new_attempts[0]

            lesson_title = user_review.get('lesson_title')
            lesson_url = user_review.get('lesson_url')
            is_lesson_failed = user_review.get('is_negative')

            send_notification(username=username, lesson_title=lesson_title, chat_id=chat_id,
                              lesson_url=lesson_url, is_lesson_failed=is_lesson_failed, telegram_bot=telegram_bot
                              )


if __name__ == '__main__':
    devman_token = os.environ.get('DEVMAN_TOKEN')
    telegram_token = os.environ.get('TG_TOKEN')
    username = os.environ.get('USERNAME')
    chat_id = os.environ.get('CHAT_ID')

    api = ApiDevMan(devman_token=devman_token)
    telegram_bot = telegram.Bot(token=telegram_token)

    user_reviews = api.get_user_reviews()
    print(user_reviews)
    api.get_long_polling(telegram_bot=telegram_bot, username=username, chat_id=chat_id)
