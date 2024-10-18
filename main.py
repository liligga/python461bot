import asyncio
import logging
from aiogram import Bot

from bot_config import bot, dp, database
from handlers.start import start_router
# from handlers.picture import picture_router
from handlers.other_messages import other_msg_router
from handlers.opros_dialog import opros_router
from handlers.admin_book_fsm import admin_book_router


async def on_startup(bot: Bot):
    print("Бот запустился")
    database.create_tables()


async def main():
    dp.include_router(start_router)
    # dp.include_router(picture_router)
    dp.include_router(opros_router)
    dp.include_router(admin_book_router)
    # в самом конце общий обработчик
    dp.include_router(other_msg_router)

    dp.startup.register(on_startup)
    # запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())