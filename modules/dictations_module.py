""" Работа с бд"""
from typing import NamedTuple, Optional, List

from modules import themes_module
import db

import exceptions


class Dictation(NamedTuple):
    """Структура одной темы"""
    id: Optional[int]
    themes_id: int
    dictation: str


class Dictations(NamedTuple):
    """Структура одной темы"""
    theme_name: str
    dicts: List[tuple]


def add_dictation(themes_id: int, dictation: str) -> Dictation:
    """Добавляет новый диктант"""

    _add_dictation_exist_check(themes_id, dictation)

    db.insert("dictations", {
        "themes_id": themes_id,
        "dictation": dictation,
    })
    return Dictation(id=None,
                     themes_id=themes_id,
                     dictation=dictation)


def get_dictations_theme(theme_id: int, show_all=0) -> list[Dictations]:
    row_dictation = None
    if show_all == 1:
        row_dictation = db.fetchall("dictations d", ["d.id", "d.themes_id", "d.dictation"],
                                    wanna_return=tuple)
    elif show_all == 0:
        row_dictation = db.fetchall("dictations d", ["d.id", "d.themes_id", "d.dictation"],
                                    wanna_return=tuple,
                                    where=f"where d.themes_id={theme_id}")
    result_dict = {}
    for d_id, th_id, dictation in row_dictation:
        th_name = themes_module.get_theme(th_id).theme_name

        if th_name in result_dict:
            result_dict[th_name].append((dictation, d_id))
        else:
            result_dict[th_name] = [(dictation, d_id)]

    dicts = [Dictations(theme_name=str(key),
                        dicts=list(value)) for key, value in result_dict.items()]
    print(dicts)
    return dicts


def _add_dictation_exist_check(themes_id: int, dictation: str) -> None:
    """Проверяет на существование названия диктанта для этой темы в БД"""

    exist_dictation = db.fetchall("dictations", ["themes_id", "dictation"], wanna_return=tuple)
    exist_dictation = set(exist_dictation)

    if (themes_id, dictation) in exist_dictation:
        raise exceptions.ExistingEntry(f"Ошибка!\n"
                                       f"Такой диктант для этой темы уже существует\n\n"
                                       f"Введите другой диктант, или нажмите /cancel")
