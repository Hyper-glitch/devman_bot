import os

from dotenv import load_dotenv

load_dotenv()

DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
USERNAME = os.getenv('USERNAME')
CHAT_ID = os.getenv('CHAT_ID')
