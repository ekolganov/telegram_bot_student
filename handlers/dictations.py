from handlers import themes
from modules import themes_module, dictations_module, shared_module
import exceptions

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


import textwrap


class Form(StatesGroup):
    wait_choose_theme = State()
    wait_dictation = State()
    wait_renamed_dictation_text = State()


async def add_dictation1(message: types.Message, state: FSMContext):
    """ Выводит список тем и предлагает выбрать к какой добавить диктант """

    await state.finish()

    await themes.list_of_themes_dictations(message)

    answer_message = (f"Вот список тем\n"
                      f"💡Нажми на add_dictation под нужной темой, чтобы добавить диктант\n\n")
    await message.answer(answer_message)
    await Form.wait_choose_theme.set()


async def add_dictation2(message: types.Message, state: FSMContext):
    """ Предлагает исправить диктант """

    theme_id = shared_module.get_id_command(message.text)
    await state.update_data(theme_id=theme_id)

    theme = themes_module.get_theme(theme_id)

    await message.answer(f"Выбрана тема:\n\n"
                         f"📒 {theme.theme_name}\n\n"
                         f"💡Напечатайте диктант")
    await state.update_data(theme_name=f"{theme.theme_name}")
    await Form.wait_dictation.set()


async def add_dictation3(message: types.Message, state: FSMContext):
    """ Добавляет диктант к теме """

    dictation = message.text
    st = await state.get_data()
    theme_id, theme_name = (st["theme_id"], st["theme_name"])

    try:
        dictations_module.add_dictation(theme_id, dictation)
    except exceptions.ExistingEntry as e:
        await message.answer(str(e))
        return

    await message.answer(f"✅Диктант добавлен в тему {theme_name}")
    await state.finish()


async def list_dictations(message: types.Message):
    """ Выводит список диктантов для каждой темы """

    theme_id = shared_module.get_id_command(message.text)
    if theme_id:
        list_dictations_theme = dictations_module.get_dictations_theme(theme_id)
    else:
        list_dictations_theme = dictations_module.get_dictations_theme(theme_id, show_all=1)

    if not list_dictations_theme:
        await message.answer("Нет ни одного диктанта")
        return

    dictations_row = []
    for d_th in list_dictations_theme:
        dictations = [f"▪ {textwrap.shorten(dictation, width=100, placeholder='...')}ℹ /full_dict{d_id} \n"
                      f"✏/rewrite_dict{d_id}   ❌/del_dict{d_id}\n"
                      for dictation, d_id in d_th.dicts]

        dictations_row += [f"📒 {d_th.theme_name}\n\n"
                           f"{shared_module.unpack_list(dictations)}"]

    answer_message = "💬Список тем и диктантов для них:\n\n"
    await message.answer(answer_message)
    await shared_module.pagination_output(message, dictations_row)


async def get_dict_full(message: types.Message):
    """ Возвращает голый текст диктанта """

    dict_id = shared_module.get_id_command(message.text)

    dictation = dictations_module.get_dict(dict_id)
    theme_name = themes_module.get_theme(dictation.themes_id)

    await message.answer(f"📒 Тема {theme_name.theme_name}\n"
                         f"Для {theme_name.themes_grade_number}а")
    await message.answer(dictation.dictation)


async def del_dict(message: types.Message):
    """ Удаляет диктант """

    dict_id = shared_module.get_id_command(message.text)

    dictations_module.del_dict(dict_id)
    await message.answer("Удалил")


async def rewrite_dict1(message: types.Message, state: FSMContext):
    """ Приглашение на исправление диктанта """

    await state.finish()

    dict_id = shared_module.get_id_command(message.text)
    await state.update_data(dict_id=f"{dict_id}")

    dictation_old = dictations_module.get_dict(dict_id)

    answer_message = (f"💬Текущий диктант:\n\n"
                      f"{dictation_old.dictation}\n\n"
                      f"✏Введите исправленный диктант заново\n"
                      f"или нажмите /cancel")

    await message.answer(answer_message)
    await Form.wait_renamed_dictation_text.set()


async def rewrite_dict2(message: types.Message, state: FSMContext):
    """ Исправляем диктант """

    await state.update_data(updated_dict=message.text)
    st = await state.get_data()

    dictations_module.rewrite_dict(st["dict_id"], st["updated_dict"])

    await state.finish()
    await message.answer("✅Диктант обновлён")


def register_handlers_dictations(dp: Dispatcher):
    """ Регистрация message handler диктантов для бота """

    dp.register_message_handler(add_dictation1, commands='add_dictation', state="*")
    dp.register_message_handler(add_dictation2,
                                lambda message: message.text.startswith('/add_dictation'), state="*")
    dp.register_message_handler(add_dictation2,
                                lambda message: message.text.startswith('/add_dictation'), state=Form.wait_choose_theme)
    dp.register_message_handler(add_dictation3, state=Form.wait_dictation)

    dp.register_message_handler(list_dictations,
                                lambda message: message.text.startswith('/dictations'), state="*")
    dp.register_message_handler(get_dict_full,
                                lambda message: message.text.startswith('/full_dict'), state="*")
    dp.register_message_handler(del_dict,
                                lambda message: message.text.startswith('/del_dict'), state="*")

    dp.register_message_handler(rewrite_dict1,
                                lambda message: message.text.startswith('/rewrite_dict'), state="*")
    dp.register_message_handler(rewrite_dict2, state=Form.wait_renamed_dictation_text)
