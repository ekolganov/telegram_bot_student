""" Работа с бд"""
import datetime
import re
from typing import List, NamedTuple, Optional
import exceptions

import pytz

import db


class Student(NamedTuple):
    """Структура студента"""
    id: Optional[int]
    fullname: str
    grade: str
    description: Optional[str]


def get_students() -> list[Student]:
    cursor = db.get_cursor()
    cursor.execute("select st.id, st.full_name, st.grade_number, st.description "
                   "from student st")
    rows = cursor.fetchall()
    students = [Student(id=row[0], fullname=row[1], grade=row[2], description=row[3]) for row in rows]
    return students


def delete_student(row_id: int) -> None:
    """Удаляет студента по его идентификатору"""
    db.delete("student", row_id)


def add_student(raw_message: str) -> Student:
    """Добавляет нового студента"""

    parsed_message = _parse_message_add_student(raw_message)

    db.insert("student", {
        "full_name": parsed_message.fullname,
        "grade_number": parsed_message.grade,
        "description": parsed_message.description,
    })
    return Student(id=None,
                   fullname=parsed_message.fullname,
                   grade=parsed_message.grade,
                   description=parsed_message.description)


def _parse_message_add_student(raw_message: str) -> Student:
    """Парсит текст пришедшего сообщения для добавления нового студента."""

    regexp_result = re.match(r"(\w+ \w+( \w+)?) (\d{1,2} класс)\s?(.*)", raw_message)

    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(3):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите текст в формате\n"
            "\n➡Вася Пупкин 6 класс"
            "\nможно с ФИО и примечанием"
            "\n➡Вася Пупкин Дмитриевич 6 класс оболутс оболтусом")

    fullname = regexp_result.group(1)
    grade = regexp_result.group(3)
    if regexp_result.group(4):
        description = regexp_result.group(4)
    else:
        description = ""

    return Student(id=None, fullname=fullname, grade=grade, description=description)
