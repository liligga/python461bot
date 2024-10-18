from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database


opros_router = Router()

# Finite State Machine = Конечный автомат
class Opros(StatesGroup):
    name = State()
    age = State()
    gender = State()
    genre = State()


@opros_router.callback_query(F.data == 'opros')
async def start_opros_handler(callback: types.CallbackQuery, state: FSMContext):
    # выставвляем состояние диалога на Opros.name
    await state.set_state(Opros.name)
    await callback.message.answer("Как Вас зовут?")

@opros_router.message(Command('stop'))
@opros_router.message(F.text == 'стоп')
async def stop_opros_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опрос остановлен!")

@opros_router.message(Opros.name)
async def process_name(message: types.Message, state: FSMContext):
    # сохраняем имя в времменный словарь
    await state.update_data(name=message.text)
    await state.set_state(Opros.age)
    await message.answer("Сколько Вам лет?")

@opros_router.message(Opros.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Вводите только цифры")
        return
    age = int(age)
    if age < 12 or age > 90:
        await message.answer("Допустимый возраст от 12 до 90")
        return
    await state.update_data(age=age)
    await state.set_state(Opros.gender)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Мужской"),
                types.KeyboardButton(text="Женский")
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Какого Вы пола?", reply_markup=kb)

@opros_router.message(Opros.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text
    if gender not in ("Мужской", "Женский"):
        await message.answer("Введите пожалуйста корректный пол")
        return
    kb = types.ReplyKeyboardRemove()
    # data = await state.get_data()
    # print(data)
    await state.update_data(gender=message.text)
    await state.set_state(Opros.genre)
    await message.answer("Отправьте Ваш любимый жанр худ литературы?", reply_markup=kb)

@opros_router.message(Opros.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    data = await state.get_data()
    tg_id = message.from_user.id
    print(data) # {'name': 'igor', 'age': 22, 'gender': ...}

    # сохранение данных введеных пользователем в БД
    database.execute(
        query="""
        INSERT INTO survey_results (name, age, gender, tg_id, genre)
        VALUES (?, ?, ?, ?, ?)
        """,
        params=(
            data["name"],
            data["age"],
            data["gender"],
            tg_id,
            data["genre"]
        )
    )

    # завершает диалог и чистит состояния
    await state.clear()
    await message.answer("Спасибо за пройденный отпрос")