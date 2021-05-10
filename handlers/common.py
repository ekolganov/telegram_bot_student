import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ResponseParameters


async def cancel_handler(message: types.Message, state: FSMContext):
    """ Отменить текущее действие в любом состоянии """

    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info(f'Cancelling state {current_state}')
    await state.finish()
    await message.answer("Отмена")


async def send_welcome(message: types.Message, state: FSMContext):
    """ Отправляет приветственное сообщение помощи по боту и создаёт кнопки помощи"""

    await state.finish()

    list_commands = [
        "Действия с учениками\n",
        "Список учеников: /students_list",
        "Добавить ученика: /add_student",
        "Список учеников и тем для их класса: /student_themes_list",
        "\nДействия с темами\n",
        "Список тем и диктантов к ним (5-9 класс): /themes_list",
        "Добавить тему: /add_theme",
        "\nДействия с диктантами\n",
        "Просмотреть все диктанты: /dictations",
        "Добавить диктант: /add_dictation",
        "\nЕГЭ\n",
        "Список заданий и материалов к ЕГЭ: /ege_tasks_list",
        "Добавить задание ЕГЭ: /add_ege_task",
    ]

    button_help = KeyboardButton('/help')
    button_cancel = KeyboardButton('/cancel')
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_help, button_cancel)

    answer_message = "💬Бот помощник в изучении русского языка:\n\n" + "\n".join(list_commands)
    await message.answer(answer_message, reply_markup=kb)


def register_handlers_common(dp: Dispatcher):
    """ Регистрация message handler для бота """

    dp.register_message_handler(send_welcome, commands=['start', 'help'], state="*")
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
