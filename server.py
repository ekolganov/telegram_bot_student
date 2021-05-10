"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import asyncio
import os

from handlers import students, themes, dictations, common, ege, share

from middlewares import AccessMiddleware

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = "1653214808:AAEBtQbr0xuXFcaingH94vjplu-8x_1qVQE"
ACCESS_ID = [344928892, 1596273768]

# API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
# ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(AccessMiddleware(ACCESS_ID))

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    common.register_handlers_common(dp)
    students.register_handlers_students(dp)
    themes.register_handlers_themes(dp)
    dictations.register_handlers_dictations(dp)
    share.register_handlers_share(dp)
    ege.register_handlers_ege(dp)

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
