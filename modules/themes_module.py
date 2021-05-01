""" Работа с бд"""
from typing import NamedTuple, List, Optional
import db
import re
import exceptions


class Theme(NamedTuple):
    """Структура одной темы"""
    id: Optional[int]
    themes_grade_number: str
    theme_name: str


class Themes(NamedTuple):
    """Структура множества тем"""
    themes_grade_number: str
    theme_names_ids: List[tuple]


def get_themes() -> list[Themes]:
    rows = db.fetchall("themes th", ["th.id", "th.themes_grade_number", "th.theme_name"],
                       wanna_return=tuple, order="ORDER BY themes_grade_number, th.theme_name")

    result_dict = {}
    for th_id, grade, th_name in rows:
        if grade in result_dict:
            result_dict[grade].append((th_name, th_id))
        else:
            result_dict[grade] = [(th_name, th_id)]

    themes = [Themes(themes_grade_number=key,
                     theme_names_ids=list(value)) for key, value in result_dict.items()]
    return themes


def delete_theme(row_id: int) -> None:
    """Удаляет студента по его идентификатору"""
    db.delete("themes", row_id)


def add_theme(theme_grade: str, theme_name: str) -> Theme:
    """Добавляет новую тему"""

    _add_theme_exist_check(theme_grade, theme_name)

    db.insert("themes", {
        "themes_grade_number": theme_grade,
        "theme_name": theme_name,
    })
    return Theme(id=None,
                 themes_grade_number=theme_grade,
                 theme_name=theme_name)


def add_theme_grade_check(raw_message: str) -> None:
    """Проверяет на соответствие название класса у темы"""

    regexp_result = re.search(r"^(\d{1,2} класс)$", raw_message)

    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите класс для темы в формате\n"
            "➡6 класс\n"
            "или нажмите /cancel")


def _add_theme_exist_check(theme_grade: str, theme_name: str) -> None:
    """Проверяет на существование названия темы для этого класса в БД"""

    exist_themes = db.fetchall("themes", ["themes_grade_number", "theme_name"], wanna_return=tuple)
    exist_themes = set(exist_themes)

    if (theme_grade, theme_name) in exist_themes:
        raise exceptions.ExistingEntry(f"Ошибка!\n"
                                       f"Такая тема для {theme_grade} класса уже есть\n\n"
                                       f"Введите другую тему, или нажмите /cancel")


def get_theme(theme_id: int) -> Theme:
    row = db.fetchone("themes th", ["th.id", "th.themes_grade_number", "th.theme_name"],
                      where=f"where th.id={theme_id}")
    return Theme(id=row[0], themes_grade_number=row[1], theme_name=row[2])


def rename_theme(theme_id: int, new_theme_name: str) -> Theme:
    updated_theme_row = db.updateone("themes", set_row=f"theme_name='{new_theme_name}'",
                                     where=f"where id={theme_id}")
    return Theme(id=updated_theme_row[0],
                 themes_grade_number=updated_theme_row[1],
                 theme_name=updated_theme_row[2])
