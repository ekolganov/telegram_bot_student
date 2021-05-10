""" Работа с бд"""
from typing import NamedTuple, Optional, List, Tuple

import db

import exceptions
import os


class EgeTask(NamedTuple):
    """ Структура задания ЕГЭ """

    id: Optional[int]
    task: str
    task_name: str


class BlobFile(NamedTuple):
    """ Структура файла с blob датой """

    blob_data: bytes
    filename: str
    extension: str


class EgeContentHard(NamedTuple):
    """ Структура контента c файлом из blob_data """

    id: Optional[int]
    task_id: int
    content_type: str
    blob_data: Optional[str]
    telegram_file_id: str
    file_fullname: str
    description: Optional[str]
    mime_type: Optional[str]
    file_full_path: str


class EgeContentLite(NamedTuple):
    """ Структура облегчённой версии контента, без выгрузки из БД фото """

    id: Optional[int]
    task_id: int
    content_type: str
    telegram_file_id: str
    description: Optional[str]


def get_ege_tasks() -> List[EgeTask]:
    """ Получить список заданий ЕГЭ """

    row_ege_tasks = db.fetchall("ege", ["id", "tasks", "tasks_name"], wanna_return=dict,
                                order="ORDER BY CAST(tasks AS UNSIGNED), tasks")

    ege_tasks = [EgeTask(id=ege_tasks["id"],
                         task=ege_tasks["tasks"],
                         task_name=ege_tasks["tasks_name"]) for ege_tasks in row_ege_tasks]
    return ege_tasks


def upload_ege_content(message_file_id: str, description: str, task_id: int, content_type: str,
                       document_filename: str = None, document_mime_type: str = None):
    """ Загружает в БД файл типа photo или document """

    if description == "/None":
        description = None
    try:
        if content_type == "document":
            blob_file = _convert_file_blob_fullname(content_type, document_filename)
            db.insert("ege_content", {
                "tasks_id": task_id,
                "content_type": content_type,
                "blob_data": blob_file.blob_data,
                "telegram_file_id": message_file_id,
                "file_name": blob_file.filename,
                "file_extension": f".{blob_file.extension}",
                "description": description,
                "mime_type": document_mime_type,
            })
        elif content_type == "photo":
            blob_file = _convert_file_blob_fullname(content_type, document_filename)
            db.insert("ege_content", {
                "tasks_id": task_id,
                "content_type": content_type,
                "blob_data": blob_file.blob_data,
                "telegram_file_id": message_file_id,
                "file_name": blob_file.filename,
                "file_extension": blob_file.extension,
                "description": description,
            })

    except Exception as ex:
        raise exceptions.NotCorrectUpload(f"Неудачная загрузка документа:\n"
                                          f"{ex.args}")


def _convert_file_blob_fullname(content_type: str, document_filename: str) -> BlobFile:
    """ конвертирует файл в blob, вытаскивает из файла имя и расширение """

    blob_data = None
    filename = None
    extension = None
    temp_path = ""

    if content_type == "document":
        temp_path = "documents"
    elif content_type == "photo":
        temp_path = "photos"

    temp_path_files = os.listdir(temp_path)

    for file in temp_path_files:
        file_full_path = os.path.join(temp_path, file)
        blob_data = db.convert_to_blob_data(file_full_path)

        if content_type == "document":
            filename, extension = document_filename.split(".")
        elif content_type == "photo":
            filename, extension = os.path.splitext(file)

    _delete_temp_files(temp_path)
    return BlobFile(blob_data=blob_data, filename=filename, extension=extension)


def get_list_ege_content_lite(task_id: int) -> Tuple[List[EgeContentLite], int]:
    """
    Возвращает список контента и его кол-во по номеру ЕГЭ задания, без выгрузки blob_data
    """

    ege_content_row = db.fetchall("ege_content", ["id", "tasks_id", "content_type", "telegram_file_id", "file_name",
                                                  "description", "file_extension"],
                                  wanna_return=tuple, where=f"WHERE tasks_id={task_id}")

    ege_content_lite = [EgeContentLite(id=row_id, task_id=task_id, content_type=content_type,
                                       telegram_file_id=telegram_file_id,
                                       description=description if description else file_name + file_extension)
                        for row_id, tasks_id, content_type, telegram_file_id,
                        file_name, description, file_extension in ege_content_row]
    content_count = len(ege_content_lite)
    return ege_content_lite, content_count


def get_ege_content_lite(ege_content_id: int) -> EgeContentLite:
    """ Возвращает контент без выгрузки из БД blob_data """

    ege_content_row = db.fetchone("ege_content", ["id", "tasks_id", "content_type", "telegram_file_id", "file_name",
                                                  "description", "file_extension"],
                                  where=f"WHERE id={ege_content_id}")
    row_id = ege_content_row[0]
    task_id = ege_content_row[1]
    content_type = ege_content_row[2]
    telegram_file_id = ege_content_row[3]
    file_name = ege_content_row[4]
    description = ege_content_row[5]
    file_extension = ege_content_row[6]

    ege_content_lite = EgeContentLite(id=row_id, task_id=task_id, content_type=content_type,
                                      telegram_file_id=telegram_file_id,
                                      description=description if description else file_name + file_extension)
    return ege_content_lite


def _delete_temp_files(temp_path: str) -> None:
    """ Удаляет все файлы в директории temp_path """

    for file in os.listdir(temp_path):
        file_full_path = os.path.join(temp_path, file)
        os.remove(file_full_path)


def get_ege_content_hard(ege_content_id: int) -> EgeContentHard:
    """ Возвращает тяжелый контент с выгрузкой из БД blob_data """

    ege_content_row = db.fetchone("ege_content", ["id", "tasks_id", "content_type", "blob_data", "telegram_file_id",
                                                  "file_name", "description", "file_extension", "mime_type"],
                                  where=f"WHERE id={ege_content_id}")
    row_id = ege_content_row[0]
    task_id = ege_content_row[1]
    content_type = ege_content_row[2]
    blob_data = ege_content_row[3]
    telegram_file_id = ege_content_row[4]
    file_name = ege_content_row[5]
    description = ege_content_row[6]
    file_extension = ege_content_row[7]
    mime_type = ege_content_row[8]
    file_fullname = file_name + file_extension

    file_full_path = _write_file_from_blob(blob_data, file_fullname)

    ege_content_hard = EgeContentHard(id=row_id, task_id=task_id, content_type=content_type, blob_data=blob_data,
                                      telegram_file_id=telegram_file_id,
                                      description=description if description else file_fullname,
                                      file_fullname=file_fullname,
                                      mime_type=mime_type, file_full_path=file_full_path)
    return ege_content_hard


def _write_file_from_blob(blob_data: bytes, file_fullname: str):
    """ записывает в файл данные из blob_data в папку documents """

    temp_path = "documents"
    file_full_path = os.path.join(temp_path, file_fullname)
    db.convert_from_blob_data(blob_data, file_full_path)
    return file_full_path


def del_ege_content(ege_content_id: int) -> None:
    """ Удаляет строку с контентом """

    db.delete("ege_content", ege_content_id)


def del_ege_task(ege_id: int) -> None:
    """ Удаляет строку с ЕГЭ заданиями и контент в задании """

    db.delete("ege", ege_id)
    db.delete_custom("ege_content", "tasks_id", ege_id)


def add_ege_task(task_name: str, task_description: str):
    """ Добавляет ЕГЭ задание """

    db.insert("ege", {
        "tasks": task_name,
        "tasks_name": task_description,
    })


def rewrite_ege_task(ege_id: int, rewrited_task: str) -> None:
    """ Обновляет название ЕГЭ темы """

    db.updateone("ege", f"tasks='{rewrited_task}'", f"where id={ege_id}")


def rewrite_content_description(ege_content_id: int, rewrited_description: str) -> None:
    """ Обновляет описание к контенту """

    db.updateone("ege_content", f"description='{rewrited_description}'", f"where id={ege_content_id}")


def rewrite_ege_name_task(ege_id: int, rewrited_ege_task_name: str) -> None:
    """ Обновляет описание/тематику ЕГЭ задания """

    db.updateone("ege", f"tasks_name='{rewrited_ege_task_name}'", f"where id={ege_id}")