import os
from dotenv import load_dotenv

load_dotenv()

WebApp_URL=os.getenv("TELEGRAM_TOKEN")
TELEGRAM_TOKEN=os.getenv('WebApp_URL')

