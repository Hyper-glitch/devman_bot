import json

import requests


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
            long_polling_response = requests.get(url=long_polling_url, headers=self.header, timeout=60)
            long_polling_response.raise_for_status()

            jsonify_response = json.loads(long_polling_response.text)
            long_polling = jsonify_response.get('results')

            for user_review in long_polling:
                print(user_review)

            return user_reviews


if __name__ == '__main__':
    api = ApiDevMan(token='***')
    user_reviews = api.get_user_reviews()
    long_polling = api.get_long_polling()
