import asyncio
import logging
from aiogram import Bot

from bot_config import bot, dp, database
from handlers import private_router
from handlers.group_bot import group_router

async def on_startup(bot: Bot):
    print("Бот запустился")
    database.create_tables()


async def main():
    dp.include_router(group_router)
    dp.include_router(private_router)


    dp.startup.register(on_startup)
    # запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())