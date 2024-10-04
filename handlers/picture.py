from aiogram import Router, types
from aiogram.filters.command import Command

picture_router = Router()

@picture_router.message(Command("pic"))
async def send_picture_handler(message: types.Message):
    image = types.FSInputFile("images/cat.jpg")
    # await message.answer_photo(
    #     photo=image,
    #     caption="Котик"
    # )
    await message.reply_photo(
        photo=image,
        caption="Котик"
    )