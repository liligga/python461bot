from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


opros_router = Router()

# Finite State Machine = Конечный автомат
class Opros(StatesGroup):
    name = State()
    age = State()
    gender = State()
    genre = State()


@opros_router.message(Command('opros'))
async def start_opros_handler(message: types.Message, state: FSMContext):
    # выставвляем состояние диалога на Opros.name
    await state.set_state(Opros.name)
    await message.answer("Как Вас зовут?")

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
    await state.update_data(age=message.text)
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
    kb = types.ReplyKeyboardRemove()
    await state.update_data(gender=message.text)
    await state.set_state(Opros.genre)
    await message.answer("Отправьте Ваш любимый жанр худ литературы?", reply_markup=kb)

@opros_router.message(Opros.genre)
async def process_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    data = await state.get_data()
    print(data)

    # завершает диалог и чистит состояния
    await state.clear()
    await message.answer("Спасибо за пройденный отпрос")