"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import asyncio

from handlers import students, themes, dictations
from middlewares import AccessMiddleware

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "1736892712:AAHDtOBkXm8t8xjgRnCMb8qfT3ZZuAG4QzY"
ACCESS_ID = [344928892, 1596273768]

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

        list_commands = [
            "Действия с учениками\n",
            "Список учеников: /students_list",
            "Добавить ученика: /add_student",
            "Список учеников и тем для их класса: /student_themes_list",
            "\nДействия с темами\n",
            "Список тем и диктантов к ним: /themes_list",
            "Добавить тему: /add_theme\n",
            "Просмотреть все диктанты: /dictations",
            "Добавить диктант: /add_dictation",
            # "Темы для изучения 5-9 классы: /themes_middle_school",
        ]

        answer_message = "💬Бот помощник в изучении русского языка:\n\n" + "\n".join(list_commands)
        await message.answer(answer_message)

        button_help = KeyboardButton('/help')
        button_cancel = KeyboardButton('/cancel')
        kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_help, button_cancel)
        await message.reply(message.text, reply_markup=kb)

    students.register_handlers_students(dp)
    themes.register_handlers_themes(dp)
    dictations.register_handlers_dictations(dp)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
