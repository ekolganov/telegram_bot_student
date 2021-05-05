import modules.shared_module
from modules import themes_module, shared_module
import exceptions

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    wait_theme_grade = State()
    wait_theme_name = State()
    wait_theme_renamed_text = State()


async def list_of_themes_dictations(message: types.Message):
    """ Выводим список тем и диктантов для них """

    list_themes = themes_module.get_themes()
    if not list_themes:
        await message.answer("Нет ни одной темы")
        return

    th_row = []
    for th in list_themes:
        grade = th.themes_grade_number
        themes = [f"📒 {th_name}\n"
                  f"✏/rename_theme{th_id}  ❌/del_theme{th_id}\n"
                  f"диктанты: 📓/dictations{th_id}\nдобавить диктант: 📓/add_dictation{th_id}\n"
                  for th_name, th_id in th.theme_names_ids]

        th_row += [f"➡ {grade}\n\n"
                   f"{modules.shared_module.unpack_list(themes)}"]

    answer_message = "💬Список тем:\n\n"
    await message.answer(answer_message)
    await shared_module.pagination_output(message, th_row)


async def del_theme(message: types.Message):
    """ Удаляет одну запись темы по её идентификатору """

    row_id = shared_module.get_id_command(message.text)

    themes_module.delete_theme(row_id)

    answer_message = "Удалил"
    await message.answer(answer_message)


async def add_theme1(message: types.Message, state: FSMContext):
    """ Приглашение на ввод класса для темы"""

    await state.finish()
    answer_message = (
        "Для какого класса тема? введите, например:\n"
        "➡6 класс"
    )

    await message.answer(answer_message)
    await Form.wait_theme_grade.set()


async def add_theme2(message: types.Message, state: FSMContext):
    """ Проверяет на соответствие темы и просит ввести название темы """

    await state.update_data(theme_grade=message.text)
    st = await state.get_data()

    try:
        themes_module.add_theme_grade_check(st["theme_grade"])
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return

    answer_message = (
        "Отлично!\n"
        "теперь введите название темы в произвольном порядке"
    )
    await message.answer(answer_message)
    await Form.wait_theme_name.set()


async def add_theme3(message: types.Message, state: FSMContext):
    """ Добавляет тему """

    await state.update_data(theme_name=message.text)
    st = await state.get_data()

    try:
        theme = themes_module.add_theme(st["theme_grade"], st["theme_name"])
    except exceptions.ExistingEntry as e:
        await message.answer(str(e))
        return

    answer_message = (
        f"✅Добавлена тема для {theme.themes_grade_number}а\n\n"
        f"📒 {theme.theme_name}"
    )

    await state.finish()
    await message.answer(answer_message)


async def rename_theme1(message: types.Message, state: FSMContext):
    """ Переименование темы, вывод текущей и приглос на ввод новой """

    theme_id = shared_module.get_id_command(message.text)

    await state.update_data(theme_id=theme_id)

    theme_old = themes_module.get_theme(theme_id)

    answer_message = (f"Текущее название:\n\n"
                      f"📒 {theme_old.theme_name}\n\n"
                      f"Введите новое название темы")
    await message.answer(answer_message)
    await Form.wait_theme_renamed_text.set()


async def rename_theme2(message: types.Message, state: FSMContext):
    """ Переименование темы на новое название"""

    await state.update_data(new_theme_name=message.text)
    st = await state.get_data()

    new_theme_name = themes_module.rename_theme(st["theme_id"], st["new_theme_name"])

    answer_message = (f"✅Отлично!\n"
                      f"Новое название:\n\n"
                      f"📒 {new_theme_name.theme_name}")

    await state.finish()
    await message.answer(answer_message)


def register_handlers_themes(dp: Dispatcher):
    """ Регистрация message handler тем для бота"""

    dp.register_message_handler(list_of_themes_dictations, commands='themes_list', state="*")
    dp.register_message_handler(del_theme, lambda message: message.text.startswith('/del_theme'), state="*")

    dp.register_message_handler(add_theme1, commands="add_theme")
    dp.register_message_handler(add_theme2, state=Form.wait_theme_grade)
    dp.register_message_handler(add_theme3, state=Form.wait_theme_name)

    dp.register_message_handler(rename_theme1, lambda message: message.text.startswith('/rename_theme'), state="*")
    dp.register_message_handler(rename_theme2, state=Form.wait_theme_renamed_text)
