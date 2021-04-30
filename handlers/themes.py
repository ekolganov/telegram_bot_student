from modules import themes_module
import exceptions

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


async def list_of_themes(message: types.Message):
    list_themes = themes_module.get_themes()
    if not list_themes:
        await message.answer("Нет ни одной темы")
        return

    th_row = []
    for th in list_themes:
        grade = th.themes_grade_number
        themes = [f"▪ {th_name}\n"
                  f"/dictations | /rename_theme | ❌/del_theme{th_id}" for th_name, th_id in th.theme_names_ids]

        th_row += [f"➡ {grade}\n"
                   f"{themes_module.unpack_list_themes(themes)}"]

    answer_message = "💬Список тем:\n\n" + "\n\n".join(th_row)
    await message.answer(answer_message)


async def del_theme(message: types.Message):
    """Удаляет одну запись темы по её идентификатору"""
    """/del_theme*, где цифры вместо * обозначают как 10:"""

    row_id = int(message.text[10:])
    themes_module.delete_theme(row_id)

    answer_message = "Удалил"
    await message.answer(answer_message)


def register_handlers_themes(dp: Dispatcher):
    dp.register_message_handler(list_of_themes, commands='themes_list', state="*")
    dp.register_message_handler(del_theme, lambda message: message.text.startswith('/del_theme'), state="*")
