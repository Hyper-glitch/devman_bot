import time
import urllib.parse as urllib
from typing import List

import requests

from tg_bot import send_notification


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
                response = requests.get(url=long_polling_url, headers=self.header, timeout=90, params=params)
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
