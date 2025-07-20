#Основной скрипт запуска бота:

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import router
from db_manager import create_tables

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Бот и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Подключаем роутер
dp.include_router(router)

if __name__ == "__main__":
    # Создание таблиц перед стартом бота
    asyncio.run(create_tables())

    # Запуск бота
    asyncio.run(dp.start_polling(bot))