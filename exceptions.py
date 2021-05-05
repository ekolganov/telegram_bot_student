"""Кастомные исключения, генерируемые приложением"""
import logging


class NotCorrectMessage(Exception):
    """Некорректное сообщение в бот, которое не удалось распарсить"""
    pass


class ExistingEntry(Exception):
    """Ошибка в бота о существующей записи"""
    pass
