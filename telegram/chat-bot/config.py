import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv(BOT_TOKEN)
BASE_URL = os.getenv(URL)