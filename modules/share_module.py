""" Вспомогательный модуль с общими функциями """
from typing import Optional
import re


def unpack_list(lst) -> str:
    """ Распаковка списка в строку """
    return "\n".join(map(str, lst))


def get_id_command(text_command_id: str) -> Optional[int]:
    """ Возвращает последнюю цифру из текста или None, для обработки команд-действий """

    try:
        match = re.search(r'(\d+)$', text_command_id)
        id_command = int(match.group(1))
        return id_command
    except:
        return None
