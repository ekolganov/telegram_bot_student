""" Работа с бд"""
from typing import NamedTuple, Optional, List

from modules import themes_module
import db

import exceptions
import logging


class Dictation(NamedTuple):
    """ Структура одной темы """

    id: Optional[int]
    themes_id: Optional[int]
    dictation: str


class Dictations(NamedTuple):
    """ Структура нескольких диктантов """

    theme_name: str
    dicts: List[tuple]


def add_dictation(themes_id: int, dictation: str) -> Dictation:
    """ Добавляет новый диктант """

    _add_dictation_exist_check(themes_id, dictation)

    db.insert("dictations", {
        "themes_id": themes_id,
        "dictation": dictation,
    })
    return Dictation(id=None,
                     themes_id=themes_id,
                     dictation=dictation)


def get_dictations_theme(theme_id: int, show_all=0) -> list[Dictations]:
    """ Выводим список диктантов по их темам """

    row_dictation = None
    if show_all == 1:
        row_dictation = db.fetchall("dictations ", ["id", "themes_id", "dictation"],
                                    wanna_return=tuple, order="ORDER BY dictation")
    elif show_all == 0:
        row_dictation = db.fetchall("dictations ", ["id", "themes_id", "dictation"],
                                    wanna_return=tuple,
                                    where=f"where themes_id={theme_id}", order="ORDER BY dictation")
    result_dict = {}
    for d_id, th_id, dictation in row_dictation:
        th_name = themes_module.get_theme(th_id).theme_name

        if th_name in result_dict:
            result_dict[th_name].append((dictation, d_id))
        else:
            result_dict[th_name] = [(dictation, d_id)]
    dicts = [Dictations(theme_name=str(key),
                        dicts=list(value)) for key, value in result_dict.items()]
    return dicts


def _add_dictation_exist_check(themes_id: int, dictation: str) -> None:
    """ Проверяет на существование названия диктанта для этой темы """

    exist_dictation = db.fetchall("dictations", ["themes_id", "dictation"], wanna_return=tuple)
    exist_dictation = set(exist_dictation)

    if (themes_id, dictation) in exist_dictation:
        logging.info(f'Trying to add exist dictation: {dictation} in theme: {themes_id}')
        raise exceptions.ExistingEntry(f"Ошибка!\n"
                                       f"Такой диктант для этой темы уже существует\n\n"
                                       f"Введите другой диктант, или нажмите /cancel")


def get_dict(dict_id: int) -> Dictation:
    """ Получаем диктант """

    row = db.fetchone("dictations", ["themes_id", "dictation"],
                      where=f"where id={dict_id}")
    return Dictation(id=dict_id, themes_id=row[0], dictation=row[1])


def del_dict(dict_id: int) -> None:
    """ Удаляет диктант """

    db.delete("dictations", dict_id)


def rewrite_dict(dict_id: int, new_dictation: str) -> Dictation:
    """ Обновляем запись диктанта и возвращает обновлённый диктант """

    updated_dictation_row = db.updateone("dictations", set_row=f"dictation='{new_dictation}'",
                                         where=f"where id={dict_id}")
    return Dictation(id=updated_dictation_row[0],
                     themes_id=updated_dictation_row[1],
                     dictation=updated_dictation_row[2])
