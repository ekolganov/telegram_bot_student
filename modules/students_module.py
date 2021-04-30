""" Работа с бд"""
import re
from typing import NamedTuple, Optional
import exceptions
import db


class Student(NamedTuple):
    """Структура студента"""
    id: Optional[int]
    fullname: str
    grade: str
    description: Optional[str]


class StudentThemes(NamedTuple):
    """ структура тем для учеников """
    id: Optional[int]
    student_fullname: str
    theme_name: list[str]


def get_students() -> list[Student]:
    """ Вывести список студентов """

    rows = db.fetchall("student st", ["st.id", "st.full_name", "st.grade_number", "st.description"],
                       wanna_return=dict)

    students = [Student(id=row["st.id"],
                        fullname=row["st.full_name"],
                        grade=row["st.grade_number"],
                        description=row["st.description"]) for row in rows]
    return students


def get_student_themes() -> list[StudentThemes]:
    """ Вывести студентов и их темы, в соответствии с калссом """
    rows = db.fetchall("student st", ["st.id", "st.full_name", "th.theme_name"],
                       wanna_return=tuple, join_on=""
                       "left join themes th on th.themes_grade_number=st.grade_number")
    result_dict = {}
    for st_id, name, theme in rows:
        if st_id in result_dict:
            result_dict[st_id].append(theme)
        else:
            result_dict[st_id] = [name, theme]

    students_and_themes = [StudentThemes(id=key,
                                         student_fullname=value[0],
                                         theme_name=list(value[1:])) for key, value in result_dict.items()]
    return students_and_themes


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
            "➡Вася Пупкин 6 класс\n"
            "можно с ФИО и примечанием\n"
            "➡Вася Пупкин Дмитриевич 6 класс оболутс оболтусом")

    fullname = regexp_result.group(1)
    grade = regexp_result.group(3)
    if regexp_result.group(4):
        description = regexp_result.group(4)
    else:
        description = ""

    return Student(id=None, fullname=fullname, grade=grade, description=description)
