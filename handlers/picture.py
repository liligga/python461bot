from aiogram import Router, types
from aiogram.filters import Command


picture_router = Router()


@picture_router.message(Command("pic"))
async def picture_handler(message: types.Message):
    image = types.FSInputFile("images/cat.jpg")
    await message.answer_photo(
        photo=image,
        caption="Котик"
    )