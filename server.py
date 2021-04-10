"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os
import db

from aiogram import Bot, Dispatcher, executor, types
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

#API_TOKEN = "1736892712:AAHDtOBkXm8t8xjgRnCMb8qfT3ZZuAG4QzY"
#ACCESS_ID = [344928892]

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот помощник в изучении русского языка\n\n"
        "Список учеников: /students_list\n"
        "Темы для изучения 5-9 классы: /themes_middle_school\n"
        "Подсказки 10-11 классы: /themes_high_school"
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
