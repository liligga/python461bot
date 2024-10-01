import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import dotenv_values
import logging

token = dotenv_values('.env')['BOT_TOKEN']
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Привет, {name}!")

@dp.message(Command("pic"))
async def send_picture(message: types.Message):
    image = types.FSInputFile("images/cat.jpg")
    await message.answer_photo(
        photo=image,
        caption="Котик"
    )

@dp.message()
async def echo_handler(message: types.Message):
    text = message.text
    await message.answer(text)



async def main():
    # запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())