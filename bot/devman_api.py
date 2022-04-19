import logging
import time
import urllib.parse as urllib
from typing import List

import requests
from requests.exceptions import ConnectionError, HTTPError, ReadTimeout

from constants import NO_NEW_INFO_LOGG, LONG_POLLING_TIMEOUT, LOST_CONNECTION_WARNING_LOGG, ERROR_LOGG_MESSAGE
from tg_bot import send_notification

logger = logging.getLogger('devman_bot')


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
        logger.info('Start long polling')

        endpoint = 'long_polling/'
        long_polling_url = urllib.urljoin(self.base_url, endpoint)
        params = None

        while True:
            try:
                response = requests.get(url=long_polling_url, headers=self.header, timeout=90, params=params)
            except ReadTimeout:
                logger.info(NO_NEW_INFO_LOGG)
                continue
            except ConnectionError:
                logger.warning(LOST_CONNECTION_WARNING_LOGG)
                time.sleep(LONG_POLLING_TIMEOUT)
                continue
            except HTTPError as error:
                logger.error(ERROR_LOGG_MESSAGE)
                logger.exception(error)
                continue

            reviews = response.json()
            status = reviews.get('status')

            if status == 'timeout':
                timestamp = reviews.get('timestamp_to_request')
                params = {'timestamp': timestamp}
                continue
            else:
                timestamp = reviews.get('last_attempt_timestamp')
                params = {'timestamp': timestamp}

            new_attempts = reviews.get('new_attempts')
            user_review = new_attempts[0]

            lesson_title = user_review.get('lesson_title')
            lesson_url = user_review.get('lesson_url')
            is_lesson_failed = user_review.get('is_negative')

            send_notification(
                username=username, lesson_title=lesson_title, chat_id=chat_id,
                lesson_url=lesson_url, is_lesson_failed=is_lesson_failed, telegram_bot=telegram_bot,
            )
