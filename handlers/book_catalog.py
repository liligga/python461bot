from aiogram import F, Router, types
from aiogram.filters import Command
from pprint import pprint

from bot_config import database

catalog_router = Router()


@catalog_router.message(Command("catalog"))
async def show_all_categories(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Приключения"),
                types.KeyboardButton(text="Фантастика")
            ],
            [
                types.KeyboardButton(text="Детектив"),
                types.KeyboardButton(text="Фентези")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите жанр ...."
    )
    await message.answer("Выберите жанр книг", reply_markup=kb)


genres = ("Приключения", "Фантастика", "Детектив", "Фентези")


# @catalog_router.message(lambda msg: msg.text in genres)

@catalog_router.message(F.text.in_(genres))
async def show_books_by_category(message: types.Message):
    genre = message.text
    print(f"{genre=}")
    books = database.fetch(
        query="SELECT * FROM books WHERE genre = ?",
        params=(genre,)
    )
    pprint(books)
    if len(books) == 0:
        await message.answer("К сожалению ничего не найдено!")
        return

    await message.answer("Наши книги:")
    for book in books:
        # msg = f"Название: {book[1]}\nЦена: {book[3]}"
        msg = f"Название: {book['name']}\nЦена: {book['price']}"
        await message.answer(msg)