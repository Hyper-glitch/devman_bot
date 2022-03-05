import os

import telegram


def send_notification(your_name, lesson_title, is_negative_result, lesson_url):
    bot = telegram.Bot(token=os.environ.get('TG_TOKEN'))

    if is_negative_result:
        result_text = "Unfortunately your work has mistakes"
    else:
        result_text = "Good job, keep going br!"

    bot.send_message(chat_id=os.environ.get('CHAT_ID'),
                     text=f"{your_name}, the teacher checked the work <<{lesson_title}>>" +
                          f"\nHere is an url for the lesson: {lesson_url}\n" + result_text
                     )
