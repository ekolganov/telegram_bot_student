from typing import List

from aiogram import types, Dispatcher
from telegram_bot_pagination import InlineKeyboardPaginator

# я знаю что это плохо, но не смог придумать ничего другого
# записывается весь список, который был передан в paginated_output
temp_text = []


async def pagination_output(message: types.Message, income_text: List[str]):
    """ Постраничный вывод списка в чат """

    global temp_text
    temp_text = income_text
    await send_current_page(message)


async def send_current_page(message: types.Message, page: int = 1):
    """ Отображает текущую страницу из списка temp_text """

    try:
        paginator = InlineKeyboardPaginator(
            len(temp_text),
            current_page=page,
            data_pattern='character#{page}'
        )
        answer_message = temp_text[page - 1]
        await message.answer(answer_message, reply_markup=paginator.markup)
    except Exception as ex:
        await message.answer("!!! Something bad with paging !!!\n"
                             f"{ex, ex.args}")


async def page_callback(call):
    """ Обработка вызова переключения страницы """

    page = int(call.data.split('#')[1])

    await call.message.delete()
    await send_current_page(call.message, page)


def register_handlers_share(dp: Dispatcher):
    """ Регистрация message handler для бота """

    dp.register_callback_query_handler(page_callback, lambda call: call.data.split('#')[0] == 'character', state="*")