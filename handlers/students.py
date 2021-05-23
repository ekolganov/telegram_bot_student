import handlers.share
import modules.share_module
from modules import students_module, share_module
import exceptions

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    wait_student = State()


async def list_of_students(message: types.Message):
    """ Выводит список учеников """

    list_students = students_module.get_students()
    if not list_students:
        await message.answer("Нет ни одного ученика")
        return

    list_students_rows = [
        f"➡ {student.fullname} | {student.grade} | {student.description}\n"
        f"❌ /del_student{student.id}"
        for student in list_students]

    answer_message = "💬Список учеников:\n\n" + "\n\n".join(list_students_rows)
    await message.answer(answer_message)


async def list_of_students_and_themes(message: types.Message):
    """ Выводит список учеников и тем, в соответствии с их классом """

    list_students_and_themes = students_module.get_student_themes()
    if not list_students_and_themes:
        await message.answer("Нет ни одной темы или ученика")
        return

    st_th_row = []
    for st_th in list_students_and_themes:
        name = st_th.student_fullname
        themes = [f"▪ {th}" for th in st_th.theme_name]

        st_th_row += [f"➡ {name}\n"
                      f"{modules.share_module.unpack_list(themes)}"]

    answer_message = "💬Список учеников и тем для его класса:\n\n"

    await message.answer(answer_message)
    await handlers.share.pagination_output(message, st_th_row)


async def del_student(message: types.Message):
    """ Удаляет одну запись студента по её идентификатору """

    row_id = share_module.get_id_command(message.text)
    students_module.delete_student(row_id)

    answer_message = "Удалил"
    await message.answer(answer_message)


async def add_student1(message: types.Message, state: FSMContext):
    """ Приглашение к вводу нового студента """

    await state.finish()
    await message.answer(
        "💡Чтобы добавить нового ученика введите его в формате\n"
        "➡Вася Пупкин 6 класс\n"
        "можно с ФИО и примечанием\n"
        "➡Вася Пупкин Дмитриевич 6 класс оболутс оболтусом\n"
    )
    await Form.wait_student.set()


async def add_student2(message: types.Message, state: FSMContext):
    """Добавляет нового студента"""

    await state.update_data(student=message.text)
    st = await state.get_data()

    try:
        student = students_module.add_student(st["student"])
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return

    answer_message = (
        f"💬Добавлен ученик\n\n"
        f"{student.fullname} | {student.grade} | {student.description}"
    )
    await state.finish()
    await message.answer(answer_message)


def register_handlers_students(dp: Dispatcher):
    """ Регистрация message handler студентов для бота"""

    dp.register_message_handler(list_of_students, commands='students_list', state="*")
    dp.register_message_handler(list_of_students_and_themes, commands='student_themes_list', state="*")
    dp.register_message_handler(del_student, lambda message: message.text.startswith('/del_student'), state="*")

    dp.register_message_handler(add_student1, commands="add_student")
    dp.register_message_handler(add_student2, state=Form.wait_student)
