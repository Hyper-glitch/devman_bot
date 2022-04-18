import logging

from bot_settings import SUCCESSFUL_REVIEW_TEXT, FAILED_REVIEW_TEXT


def send_notification(username, lesson_title, is_lesson_failed, lesson_url, telegram_bot, chat_id):
    """Send notification to user depending on Devman API response with lessons reviews."""
    if is_lesson_failed:
        text = FAILED_REVIEW_TEXT
    else:
        text = SUCCESSFUL_REVIEW_TEXT

    telegram_bot.send_message(
        chat_id=chat_id,
        text=f'{username}, the teacher checked the work <<{lesson_title}>>'
             + f'\nHere is an url for the lesson: {lesson_url}\n' + text,
    )


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
