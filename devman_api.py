import json
import os
from typing import List

import requests

from tg_bot import send_notification


class ApiDevMan:
    def __init__(self, token):
        self.base_url = 'https://dvmn.org/api/'
        self.token = token
        self.header = {'Authorization': 'Token ' + self.token}

    def get_user_reviews(self) -> List:
        user_reviews_url = self.base_url + 'user_reviews/'
        user_reviews_response = requests.get(url=user_reviews_url, headers=self.header)
        user_reviews_response.raise_for_status()

        user_reviews_text = json.loads(user_reviews_response.text)
        user_reviews = user_reviews_text.get('results')

        return user_reviews

    def get_long_polling(self):
        long_polling_url = self.base_url + 'long_polling/'

        while True:
            try:
                long_polling_response = requests.get(url=long_polling_url, headers=self.header, timeout=90)
                long_polling_text = json.loads(long_polling_response.text)
                timestamp = long_polling_text.get('timestamp_to_request')

                long_polling_response_timestamp = requests.get(url=long_polling_url, headers=self.header,
                                                               timeout=90, params={'timestamp': timestamp},
                                                               )
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                continue

            long_polling_text = json.loads(long_polling_response_timestamp.text)
            long_polling_response = long_polling_text.get('new_attempts')

            lesson_title = long_polling_response[0].get('lesson_title')
            lesson_url = long_polling_response[0].get('lesson_url')
            is_lesson_failed = long_polling_response[0].get('is_negative')

            send_notification(username=os.environ.get('USERNAME'), lesson_title=lesson_title,
                              lesson_url=lesson_url, is_lesson_failed=is_lesson_failed,
                              )


if __name__ == '__main__':
    api = ApiDevMan(token=os.environ.get('DEVMAN_TOKEN'))
    user_reviews = api.get_user_reviews()
    print(user_reviews)
    api.get_long_polling()
