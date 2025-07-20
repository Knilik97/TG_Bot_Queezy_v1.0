import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные среды из .env

API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
DB_NAME = 'quiz_bot.db'