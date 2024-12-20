from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database


class BookForm(StatesGroup):
    name = State()
    price = State()
    author = State()
    genre = State()
    confirm = State()


class GenreForm(StatesGroup):
    name = State()


admin = 243154734
admin_book_router = Router()
admin_book_router.message.filter(F.from_user.id == admin)


@admin_book_router.message(Command("newgenre"))
async def add_new_genre(message: types.Message, state: FSMContext):
    await state.set_state(GenreForm.name)
    await message.answer("Задайте название нового жанра:")


@admin_book_router.message(GenreForm.name)
async def process_genre_name(message: types.Message, state: FSMContext):
    name = message.text
    database.execute(
        query="INSERT INTO genres(name) VALUES (?)",
        params=(name,),
    )
    await state.clear()
    await message.answer("Жанр был успешно добавлен")


@admin_book_router.message(Command("newbook"))
async def start_book_form(message: types.Message, state: FSMContext):
    await state.set_state(BookForm.name)
    await message.answer("Задайте название книги:")


@admin_book_router.message(BookForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookForm.price)
    await message.answer("Задайте цену книги:")


@admin_book_router.message(BookForm.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(BookForm.author)
    await message.answer("Кто автор этой книги:")

l = [1, 2, 3, 4]
squares = [i**2 for i in l] # list comprehension

@admin_book_router.message(BookForm.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(BookForm.genre)
    genres = database.fetch(
        query="SELECT name FROM genres"
    ) # [{'name': 'Прирвамавв'}]
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=genre['name']) for genre in genres],
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите жанр:", reply_markup=kb)


@admin_book_router.message(BookForm.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    data = await state.get_data()
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]],
        resize_keyboard=True
    )
    await state.set_state(BookForm.confirm)
    await message.answer(f"Правильно ли вы ввели:\n Название: {data['name']},\n Цена: {data['price']},\n"
                         f" Автор: {data['author']},\n Жанр: {data['genre']}", reply_markup=kb)


@admin_book_router.message(BookForm.confirm, F.text == "Да")
async def process_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    genre = database.fetch(
        query="SELECT id FROM genres WHERE name = ?",
        params=(data['genre'],)
    ) # [{'id': 1}]
    genre_id = genre[0]['id']
    # save to db
    database.execute(
        query="""
            INSERT INTO books (name, author, price, genre_id)
            VALUES (?, ?, ?, ?)
        """,
        params=(
            data['name'],
            data['author'],
            data['price'],
            genre_id
        )
    )
    await state.clear()
    kb = types.ReplyKeyboardRemove()
    await message.answer("Данные были сохранены!", reply_markup=kb)


@admin_book_router.message(BookForm.confirm, F.text == "Нет")
async def process_not_confirmed(message: types.Message, state: FSMContext):
    await state.set_state(BookForm.name)
    await message.answer("Задайте название книги:")
