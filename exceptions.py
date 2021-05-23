"""Кастомные исключения, генерируемые приложением"""


class NotCorrectMessage(Exception):
    """Некорректное сообщение в бот, которое не удалось распарсить"""
    pass


class ExistingEntry(Exception):
    """Ошибка в бота о существующей записи"""
    pass


class NotCorrectUpload(Exception):
    """Ошибка в бота о неудачной загрузке документа"""
    pass
