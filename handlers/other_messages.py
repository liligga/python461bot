from aiogram import Router, types


other_msg_router = Router()

@other_msg_router.message()
async def other_messages_handler(message: types.Message):
    # text = message.text
    await message.answer("Извините, я вас не понимаю")
