import json
import os

import requests

from tg_bot import send_notification


class ApiDevMan:
    def __init__(self, token):
        self.base_url = 'https://dvmn.org/api/'
        self.token = token
        self.header = {'Authorization': 'Token ' + self.token}

    def get_user_reviews(self):
        user_reviews_url = self.base_url + 'user_reviews/'
        user_reviews_response = requests.get(url=user_reviews_url, headers=self.header)
        user_reviews_response.raise_for_status()

        jsonify_response = json.loads(user_reviews_response.text)
        user_reviews = jsonify_response.get('results')

        for user_review in user_reviews:
            print(user_review)

        return user_reviews

    def get_long_polling(self):
        while True:
            long_polling_url = self.base_url + 'long_polling/'
            try:
                long_polling_response = requests.get(url=long_polling_url, headers=self.header, timeout=90)
                jsonify_response = json.loads(long_polling_response.text)
                timestamp = jsonify_response.get('timestamp_to_request')

                long_polling_response_timestamp = requests.get(url=long_polling_url, headers=self.header,
                                                               timeout=90, params={'timestamp': timestamp},
                                                               )
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                continue

            jsonify_response = json.loads(long_polling_response_timestamp.text)
            long_polling_response = jsonify_response.get('new_attempts')

            lesson_title = long_polling_response[0].get('lesson_title')
            lesson_url = long_polling_response[0].get('lesson_url')
            is_negative_result = long_polling_response[0].get('is_negative')

            send_notification(your_name='Roman', lesson_title=lesson_title,
                              lesson_url=lesson_url, is_negative_result=is_negative_result,
                              )

            return user_reviews


if __name__ == '__main__':
    api = ApiDevMan(token=os.environ.get('DEVMAN_TOKEN'))
    user_reviews = api.get_user_reviews()
    long_polling = api.get_long_polling()
