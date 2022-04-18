import os

from dotenv import load_dotenv

load_dotenv()

DEVMAN_TOKEN = os.getenv('DEVMAN_TOKEN')
TELEGRAM_TOKEN = os.getenv('TG_TOKEN')
USERNAME = os.getenv('USERNAME')
CHAT_ID = os.getenv('CHAT_ID')
LONG_POLLING_TIMEOUT = 180
NO_NEW_INFO_LOGG = 'New information from Devman API has not received.'
LOST_CONNECTION_WARNING_LOGG = f'Connection lost! Retrying in {LONG_POLLING_TIMEOUT} seconds.'
ERROR_LOGG_MESSAGE = 'Bot crashed with mistake: '
SUCCESSFUL_REVIEW_TEXT = 'Good job, keep going br!'
FAILED_REVIEW_TEXT = 'Unfortunately your work has mistakes'
