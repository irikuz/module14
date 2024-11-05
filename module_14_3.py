from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import asyncio


api = "   "
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]

    ]
)
inline_menu_product = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]

    ]
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=inline_menu)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161")
    await call.answer()

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    a = int(data["weight"])
    b = int(data["growth"])
    c = int(data["age"])
    norma = 10*a+6.25*b-5*c+-161
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()

@dp.message_handler(text=["Купить"])
async def get_buying_list(message):
    with open('/Users/Shared/Previously Relocated Items/Security/Рабочая/Pyton/Project13/1.png', "rb") as img1:
        await message.answer_photo(img1,
                                   f'Название: Product1 | Описание: описание 1 | Цена: 20р')
    with open('/Users/Shared/Previously Relocated Items/Security/Рабочая/Pyton/Project13/2.png', "rb") as img2:
        await message.answer_photo(img2,
                                   f'Название: Product2 | Описание: описание 2 | Цена: 100р')
    with open('/Users/Shared/Previously Relocated Items/Security/Рабочая/Pyton/Project13/3.png', "rb") as img3:
        await message.answer_photo(img3,
                                   f'Название: Product3 | Описание: описание 3 | Цена: 200р')
    with open('/Users/Shared/Previously Relocated Items/Security/Рабочая/Pyton/Project13/4.png', "rb") as img4:
        await message.answer_photo(img4,
                                   f'Название: Product4 | Описание: описание 4 | Цена: 250р')
    await message.answer('Выберите продукт для покупки:', reply_markup=inline_menu_product)


@dp.callback_query_handler(text="product_buying")
async def end_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=start_menu)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
