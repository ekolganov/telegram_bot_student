""" Работа с бд"""
from typing import NamedTuple, List
import db


class Themes(NamedTuple):
    """Структура темы"""
    themes_grade_number: str
    theme_names_ids: List[tuple]


def unpack_list_themes(lst):
    return "\n".join(map(str, lst))


def get_themes() -> list[Themes]:
    rows = db.fetchall("themes th", ["th.id", "th.themes_grade_number", "th.theme_name"],
                       wanna_return=tuple)

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
