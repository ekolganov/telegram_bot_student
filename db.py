import os
from typing import Dict, List, Tuple

import sqlite3

conn = sqlite3.connect(os.path.join("db", "students.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict) -> None:
    """ Вставляет записи """

    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str], wanna_return: tuple or dict, join_on="", where="", order="") -> List[Tuple or Dict]:
    """
    Получает список кортежей или словарь, в зависимости от переменной wanna_return.
    Для извлечения нескольких значений
    Можно указать join_on, where, order по расположению в f-строке.
    """

    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} {where} {join_on} {order}")
    rows = cursor.fetchall()
    result = []
    if wanna_return == dict:
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result
    elif wanna_return == tuple:
        return rows


def fetchone(table: str, columns: List[str], where="") -> Tuple:
    """ Извлекает строку """

    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} {where}")
    row = cursor.fetchone()
    return row


def updateone(table: str, set_row: str, where: str) -> Tuple:
    """ Обновляет запись и возвращает обновлённую строку """

    cursor.execute(f"UPDATE {table} SET {set_row} {where}")
    conn.commit()
    cursor.execute(f"SELECT * FROM {table} {where}")
    updated_row = cursor.fetchone()
    return updated_row


def delete(table: str, row_id: int) -> None:
    """ Удаляет строку """

    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    """ Возвращает объект коннектора к БД, сахар"""

    return cursor


def _init_db() -> None:
    """Инициализирует БД"""

    with open("createdb.sql", "r", encoding="utf8") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД (есть ли таблица students), если нет — инициализирует"""

    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='students'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
