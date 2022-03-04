import os

import telegram


def send_notification(your_name):
    bot = telegram.Bot(token=os.environ.get('TG_TOKEN'))
    bot.send_message(chat_id=os.environ.get('CHAT_ID'), text=f"{your_name}, the teacher checked the work!")
