from aiogram import Router, F, types
from aiogram.filters import Command

group_router = Router()
group_router.message.filter(F.chat.type != 'private')
group_router.callback_query.filter(F.chat.type != 'private')

@group_router.message(Command("start"))
async def start_group_handler(message: types.Message):
    await message.answer("Привет, друг!")

BAD_WORDS = (
    "дурак", "тупой"
)

"Привет тупой дурак "

@group_router.message()
async def check_bad_words_handler(message: types.Message):
    txt = message.text
    words = txt.split() # ["Привет", "дурак"]
    for w in words:
        if w in BAD_WORDS:
            # нашли плохое слово
            await message.delete()
            await message.reply("Использовано запрещенное слово")
            break


