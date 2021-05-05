from typing import Optional
import re

from aiogram import Dispatcher, types
from typing import List

from telegram_bot_pagination import InlineKeyboardPaginator

# я знаю что это плохо, но не смог придумать ничего другого
temp_text = []


def unpack_list(lst) -> str:
    """ Распаковка списка на строки """

    return "\n".join(map(str, lst))


def get_id_command(text_command_id: str) -> Optional[int]:
    """ Возвращает последнюю цифру из текста или None, для обработки команд-действий """

    try:
        match = re.search(r'(\d+)$', text_command_id)
        return int(match.group(1))
    except:
        return None


async def pagination_output(message: types.Message, income_text: List[str]):
    """ Постраничный вывод списка в чат """

    global temp_text
    temp_text = income_text
    await send_current_page(message)


async def send_current_page(message: types.Message, page=1):
    """ Отображает текущую страницу из списка temp_text """

    try:
        # print(temp_text)
        paginator = InlineKeyboardPaginator(
            len(temp_text),
            current_page=page,
            data_pattern='character#{page}'
        )
        # print(len(message))
        answer_message = temp_text[page - 1]
    except:
        await message.answer("!!! Something bad with paging !!!")
    await message.answer(answer_message, reply_markup=paginator.markup)


async def page_callback(call):
    """ Обработка вызова переключения страницы """

    page = int(call.data.split('#')[1])

    await call.message.delete()
    await send_current_page(call.message, page)


def register_handlers_shared_module(dp: Dispatcher):
    """ Регистрация message handler для бота """

    dp.register_message_handler(send_current_page, state="*")
    dp.register_callback_query_handler(page_callback, lambda call: call.data.split('#')[0] == 'character', state="*")
