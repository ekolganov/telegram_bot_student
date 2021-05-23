import handlers.share
from modules import share_module, ege_module
from typing import BinaryIO

import exceptions

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    """ Состояния для модуля """

    wait_add_ege_task_name = State()
    wait_add_ege_task_description = State()

    wait_rewrite_ege_task = State()

    wait_rewrite_content_description = State()

    wait_rewrite_ege_name_task = State()

    wait_content_upload = State()
    wait_content_description = State()


async def get_list_ege_tasks(message: types.Message):
    """ Выводит список заданий и контента к ЕГЭ """

    list_ege_tasks = ege_module.get_ege_tasks()

    if not list_ege_tasks:
        await message.answer("Нет ни одного задания")
        return

    ege_tasks_row = []
    for ege_task in list_ege_tasks:
        list_ege_content_lite, content_count = ege_module.get_list_ege_content_lite(ege_task.id)

        ege_content = [f"📌Тип материала: {ege_content.content_type}\n"
                       f"Описание: {ege_content.description}\n"
                       f"ℹ /get_content_ege{ege_content.id}\n"
                       f"✏/rewrite_content_description{ege_content.id}\n"
                       f"❌/del_ege_content{ege_content.id}\n"
                       for ege_content in list_ege_content_lite]

        ege_tasks_row += [f"📔 {ege_task.task}  ✏/rewrite_ege_task{ege_task.id} ❌/del_ege_task{ege_task.id}\n"
                          f"▪ {ege_task.task_name}\n"
                          f"✏/rewrite_ege_name_task{ege_task.id}\n\n"
                          f"Добавить материалы /add_ege_content{ege_task.id}\n\n"
                          f"Всего материалов: {content_count}\n\n"
                          f"{share_module.unpack_list(ege_content)}"]

    answer_message = "💬Список заданий ЕГЭ:\n\n"
    await message.answer(answer_message)
    await handlers.share.pagination_output(message, ege_tasks_row)


async def upload_content1(message: types.Message, state: FSMContext):
    """ Приглашение на отправку контента """

    await state.finish()

    task_id = share_module.get_id_command(message.text)
    await state.update_data(task_id=task_id)

    await message.answer("Вставьте или перешлите мне одну фотографию или документ\n"
                         "Убедитесь, что название файла не содержит точек, кроме той, что обозначает расширение")
    await Form.wait_content_upload.set()


async def upload_content2(message: types.Message, state: FSMContext):
    """ Скачивание контента и передача состояний дальше"""

    if message.content_type == "document":
        bo: BinaryIO = await message.document.download()
        bo.close()
        await state.update_data(file_id=str(message.document.file_id),
                                document_file_name=str(message.document.file_name),
                                document_mime_type=str(message.document.mime_type))
    elif message.content_type == "photo":
        bo: BinaryIO = await message.photo[-1].download()
        bo.close()
        await state.update_data(file_id=str(message.photo[-1].file_id))

    await state.update_data(content_type=str(message.content_type))

    await message.answer("Введите описание для загруженного материала:\n"
                         "или нажмите /None - без описания")
    await Form.wait_content_description.set()


async def upload_content3(message: types.Message, state: FSMContext):
    """ Загрузка контента в БД """

    await state.update_data(description=str(message.text))
    st = await state.get_data()

    try:
        if st["content_type"] == "photo":
            ege_module.upload_ege_content(st["file_id"], st["description"], st["task_id"], st["content_type"])
        elif st["content_type"] == "document":
            ege_module.upload_ege_content(st["file_id"], st["description"], st["task_id"], st["content_type"],
                                          st["document_file_name"], st["document_mime_type"])
    except exceptions.NotCorrectUpload as e:
        await message.answer(str(e))
        return
    await message.answer("✅Готово")
    await state.finish()


async def get_ege_content(message: types.Message):
    """ Отправляет юзеру фото или документ по telegram_file_id """

    ege_content_id = share_module.get_id_command(message.text)

    content = ege_module.get_ege_content_lite(ege_content_id)

    try:
        if content.content_type == "photo":
            await message.answer_photo(content.telegram_file_id, content.description)
        elif content.content_type == "document":
            await message.answer_document(content.telegram_file_id, content.description)
    except Exception as ex:
        await message.answer(f"Проблема с выгрузкой контента, {ex, ex.args}")


async def del_ege_content(message: types.Message):
    """ Удаляет контент """

    ege_content_id = share_module.get_id_command(message.text)
    ege_module.del_ege_content(ege_content_id)

    await message.answer("Удалил")


async def rewrite_ege_task1(message: types.Message, state: FSMContext):
    """ Приглашение на изменение название ЕГЭ задания """

    await state.finish()
    ege_id = share_module.get_id_command(message.text)
    await state.update_data(ege_id=ege_id)
    await message.answer("Введите новое название задания:")
    await Form.wait_rewrite_ege_task.set()


async def rewrite_ege_task2(message: types.Message, state: FSMContext):
    """ Изменение название ЕГЭ задания """

    rewrited_task = message.text
    st = await state.get_data()

    ege_module.rewrite_ege_task(st["ege_id"], rewrited_task)
    await message.answer("✅Название задание изменено")

    await state.finish()


async def del_ege_task(message: types.Message):
    """ Удаляет ЕГЭ задание и его контент """

    ege_id = share_module.get_id_command(message.text)
    ege_module.del_ege_task(ege_id)
    await message.answer("Задание и материалы к нему удалены")


async def add_ege_task1(message: types.Message, state: FSMContext):
    """ Приглашение добавить задание ЕГЭ """

    await state.finish()

    await message.answer("Введите номер задания:\n"
                         "например, 1 задание")
    await Form.wait_add_ege_task_name.set()


async def add_ege_task2(message: types.Message, state: FSMContext):
    """ Приглашение добавить описание ЕГЭ задания"""

    await state.update_data(tasks=message.text)
    await message.answer("Введите тему/описание задания:")
    await Form.wait_add_ege_task_description.set()


async def add_ege_task3(message: types.Message, state: FSMContext):
    """ Добавление ЕГЭ задания """

    await state.update_data(tasks_description=message.text)
    st = await state.get_data()

    ege_module.add_ege_task(st["tasks"], st["tasks_description"])

    await message.answer("✅Задание добавлено")
    await state.finish()


async def rewrite_content_description1(message: types.Message, state: FSMContext):
    """ Приглашение на переименование описания контента """

    await state.finish()

    ege_content_id = share_module.get_id_command(message.text)
    await state.update_data(ege_content_id=ege_content_id)

    await message.answer("Введите новое описание к материалу:")
    await Form.wait_rewrite_content_description.set()


async def rewrite_content_description2(message: types.Message, state: FSMContext):
    """ Переименование описания контента """

    st = await state.get_data()
    rewrited_content = message.text

    ege_module.rewrite_content_description(st["ege_content_id"], rewrited_content)

    await message.answer("✅Описание к материалу обновлено")
    await state.finish()


async def rewrite_ege_name_task1(message: types.Message, state: FSMContext):
    """ Приглашение на переименование описания/тематики ЕГЭ задания """

    await state.finish()

    ege_id = share_module.get_id_command(message.text)
    await state.update_data(ege_id=ege_id)

    await message.answer("Введите новое описание/тематику ЕГЭ задания")
    await Form.wait_rewrite_ege_name_task.set()


async def rewrite_ege_name_task2(message: types.Message, state: FSMContext):
    """ Переименование описания/тематики ЕГЭ задания """

    st = await state.get_data()
    rewrited_ege_name_task = message.text

    ege_module.rewrite_ege_name_task(st["ege_id"], rewrited_ege_name_task)

    await message.answer("✅Описание/тематика ЕГЭ задания обновлено")
    await state.finish()


def register_handlers_ege(dp: Dispatcher):
    """ Регистрация message handler для бота """

    dp.register_message_handler(add_ege_task1, commands='add_ege_task', state="*")
    dp.register_message_handler(add_ege_task2, state=Form.wait_add_ege_task_name)
    dp.register_message_handler(add_ege_task3, state=Form.wait_add_ege_task_description)

    dp.register_message_handler(upload_content1, lambda message: message.text.startswith('/add_ege_content'), state="*")
    dp.register_message_handler(upload_content2, state=Form.wait_content_upload, content_types=['photo', "document"])
    dp.register_message_handler(upload_content3, state=Form.wait_content_description)

    dp.register_message_handler(get_list_ege_tasks, commands='ege_tasks_list', state="*")
    dp.register_message_handler(get_ege_content,
                                lambda message: message.text.startswith('/get_content_ege'), state="*")
    dp.register_message_handler(del_ege_content,
                                lambda message: message.text.startswith('/del_ege_content'), state="*")
    dp.register_message_handler(del_ege_task, lambda message: message.text.startswith('/del_ege_task'), state="*")

    dp.register_message_handler(rewrite_content_description1,
                                lambda message: message.text.startswith('/rewrite_content_description'), state="*")
    dp.register_message_handler(rewrite_content_description2, state=Form.wait_rewrite_content_description)

    dp.register_message_handler(rewrite_ege_task1,
                                lambda message: message.text.startswith('/rewrite_ege_task'), state="*")
    dp.register_message_handler(rewrite_ege_task2, state=Form.wait_rewrite_ege_task)

    dp.register_message_handler(rewrite_ege_name_task1,
                                lambda message: message.text.startswith('/rewrite_ege_name_task'), state="*")
    dp.register_message_handler(rewrite_ege_name_task2, state=Form.wait_rewrite_ege_name_task)
