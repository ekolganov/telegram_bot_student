"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import students
import exceptions

from aiogram import Bot, Dispatcher, executor, types
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

API_TOKEN = "1736892712:AAHDtOBkXm8t8xjgRnCMb8qfT3ZZuAG4QzY"
ACCESS_ID = [344928892]

#API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
#ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")

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
        
        "\n💡Чтобы добавить нового ученика введите его в формате"
        "\n➡Вася Пупкин 6 класс"
        "\nможно с ФИО и примечанием"
        "\n➡Вася Пупкин Дмитриевич 6 класс оболутс оболтусом"
    )


@dp.message_handler(commands=['students_list'])
async def list_of_students(message: types.Message):
    list_students = students.get_students()
    if not list_students:
        await message.answer("Нет ни одного ученика")
        return

    list_students_rows = [
        f"➡ {student.fullname} | {student.grade} | {student.description}\n"
        f"удалить {student.fullname} ❌ /del{student.id}"
        for student in list_students]

    answer_message = "💬Список учеников:\n\n" + "\n\n".join(list_students_rows)
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись студента по её идентификатору"""
    """сообщение будет /del*, где цифры вместо * обозначают как 4:"""

    row_id = int(message.text[4:])
    students.delete_student(row_id)

    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler()
async def add_student(message: types.Message):
    """Постоянно слушает чат и добавляет нового студента"""

    try:
        student = students.add_student(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"💬Добавлен ученик\n\n"
        f"{student.fullname} | {student.grade} | {student.description}"
    )
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
