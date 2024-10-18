from aiogram import Router, F, types
# from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.filters.command import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    # await message.answer(f"Привет, {name}!")
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text=f"Привет, {name}!"
    # )
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://geeks.kg"
                ),
                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://instagram.com/geekskg"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="О нас",
                    callback_data="aboutus"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Пройти наш опрос",
                    callback_data="opros"
                )
            ]
        ]
    )
    await message.reply(
        f"Привет, {name}. Добро пожаловать в наш бот для книголюбов",
        reply_markup=kb
    )

# @start_router.callback_query(lambda cb: cb.data == "aboutus")
@start_router.callback_query(F.data == "aboutus")
async def about_us_handler(callback: types.CallbackQuery):
    text = "Текст о нашем магазине"
    # await callback.answer(text)
    await callback.message.answer(text)