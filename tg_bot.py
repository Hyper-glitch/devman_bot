import os

import telegram


def send_notification(username, lesson_title, is_lesson_failed, lesson_url):
    bot = telegram.Bot(token=os.environ.get('TG_TOKEN'))

    if is_lesson_failed:
        text = "Unfortunately your work has mistakes"
    else:
        text = "Good job, keep going br!"

    bot.send_message(chat_id=os.environ.get('CHAT_ID'),
                     text=f"{username}, the teacher checked the work <<{lesson_title}>>" +
                          f"\nHere is an url for the lesson: {lesson_url}\n" + text
                     )
