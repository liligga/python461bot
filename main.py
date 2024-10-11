import asyncio
import logging

from bot_config import bot, dp
from handlers.start import start_router
# from handlers.picture import picture_router
from handlers.other_messages import other_msg_router
from handlers.opros_dialog import opros_router


async def main():
    dp.include_router(start_router)
    # dp.include_router(picture_router)
    dp.include_router(opros_router)
    # в самом конце общий обработчик
    dp.include_router(other_msg_router)

    # запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())