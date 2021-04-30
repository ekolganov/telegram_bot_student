"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import asyncio

from handlers import students, themes
from middlewares import AccessMiddleware

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

API_TOKEN = "1736892712:AAHDtOBkXm8t8xjgRnCMb8qfT3ZZuAG4QzY"
ACCESS_ID = [344928892]

# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(AccessMiddleware(ACCESS_ID))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        """Отменить текущее действие в любом состоянии"""
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await message.answer("Отмена")

    @dp.message_handler(commands=['start', 'help'], state="*")
    async def send_welcome(message: types.Message):
        """Отправляет приветственное сообщение и помощь по боту"""

        await message.answer(
            "Бот помощник в изучении русского языка\n\n"
            "Список учеников: /students_list\n"
            "Список тем: /themes_list\n"
            "Список учеников и тем для их класса: /student_themes_list\n"
            "Добавить студента: /add_student\n"
            "Темы для изучения 5-9 классы: /themes_middle_school\n"
        )

    students.register_handlers_students(dp)
    themes.register_handlers_themes(dp)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
