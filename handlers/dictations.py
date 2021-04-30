from handlers import themes
from modules import themes_module
from modules import dictations_module
import exceptions

from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    wait_choose_theme = State()
    wait_dictation = State()


async def add_dictation1(message: types.Message, state: FSMContext):
    await state.finish()

    await themes.list_of_themes(message)

    answer_message = (f"Вот список тем\n"
                      f"Нажми на add_dictation под нужной темой, чтобы добавить диктант\n\n")
    await message.answer(answer_message)
    await Form.wait_choose_theme.set()


async def add_dictation2(message: types.Message, state: FSMContext):
    theme_id = int(message.text[14:])
    await state.update_data(theme_id=theme_id)

    theme = themes_module.get_theme(theme_id)

    await message.answer(f"Выбрана тема {theme.theme_name}\n"
                         f"Напечатайте диктант")
    await Form.wait_dictation.set()


async def add_dictation3(message: types.Message, state: FSMContext):
    dictation = message.text
    st = await state.get_data()

    try:
        dictations_module.add_dictation(st["theme_id"], dictation)
    except exceptions.ExistingEntry as e:
        await message.answer(str(e))
        return

    await message.answer(f"Диктант добавлен в тему")
    await state.finish()


async def list_dictations(message: types.Message):
    theme_id = message.text[11:]
    if theme_id:
        list_dictations_theme = dictations_module.get_dictations_theme(theme_id)
    else:
        list_dictations_theme = dictations_module.get_dictations_theme(theme_id, show_all=1)

    if not list_dictations_theme:
        await message.answer("Нет ни одного диктанта")
        return

    dictations_row = []
    for d_th in list_dictations_theme:
        dictations = [f"▪ {dictantion}\n"
                      f"ℹ /alone_dict{d_id}   ✏/rewrite_dict{d_id}   ❌/del_dict{d_id}\n"
                      for dictantion, d_id in d_th.dicts]

        dictations_row += [f"➡ {d_th.theme_name}\n"
                           f"{themes_module.unpack_list(dictations)}"]

    answer_message = "💬Список тем и диктантов для них:\n\n" + "\n\n".join(dictations_row)
    await message.answer(answer_message)


def register_handlers_dictations(dp: Dispatcher):
    dp.register_message_handler(add_dictation1, commands='add_dictation', state="*")
    dp.register_message_handler(add_dictation2,
                                lambda message: message.text.startswith('/add_dictation'),
                                state="*")
    dp.register_message_handler(add_dictation2,
                                lambda message: message.text.startswith('/add_dictation'),
                                state=Form.wait_choose_theme)
    dp.register_message_handler(add_dictation3, state=Form.wait_dictation)
    dp.register_message_handler(list_dictations,
                                lambda message: message.text.startswith('/dictations'),
                                state="*")
