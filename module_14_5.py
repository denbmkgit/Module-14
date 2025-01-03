from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
from apies import UrbanBotDen_2
from keyboards import product_kb
from admin_d_3 import *
from db_d_3 import *
from crud_functions import get_all_products
import crud_functions

api = UrbanBotDen_2
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text="Рассчитать")
button2 = KeyboardButton(text="Информация")
button_buy = KeyboardButton(text="Купить")
button_regisration = KeyboardButton(text="Регистрация")
kb.row(button1, button2)
kb.row(button_regisration, button_buy)

kb_in_line = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Расчитать норму колорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb_in_line.add(button3)
kb_in_line.add(button4)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in_line)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: '
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5,  '
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


str_warning = "Задавайте только целые числа"
str_wrong_input = "вводите Только латиские буквы и цифры"


def calories_calculate(data):
    calories_for_male = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    calories_for_female = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161
    return calories_for_male, calories_for_female


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()

    if crud_functions.is_included(data['username']) == True:
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    # data = await state.get_data()
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    if not data['age'].isdigit():
        await message.answer(str_warning)
    else:
        crud_functions.add_user(data['username'], data['email'], data['age'])


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer(f'Привет {message.from_user.username} ! Я бот умеющий расчитать колории для тебя.',
                         reply_markup=kb)


@dp.message_handler(text=["Информация"])
async def information(message):
    await message.answer("Я бот помогающий твоему здоровью, расчитывая необходимую для тебя норму потребления колорий "
                         "используя упрощённую формулу Миффлина - Сан Жеора. "
                         "Так же у накс можно заказать витаминки, нажав кнопку Купить", reply_markup=kb)


get_all_products()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in get_all_products():
        with open(f'files/{i[0]}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: {i[1]} | {i[2]} | {i[3]}')
    with open('files/M.png', 'rb') as img:
        await message.answer_photo(img, 'Выберете продукт для покупки:', reply_markup=product_kb)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text=["calories"])
async def set_age(call):
    await call.message.answer("Укажите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()

    if not data['age'].isdigit():
        await message.answer(str_warning)
    else:
        await message.answer(f"Ваш возраст: {data['age']}. Укажите свой рост:")
        await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()

    if not data['growth'].isdigit():
        await message.answer(str_warning)
    else:
        await message.answer(f"Ваш рост: {data['growth']}, Укажите свой вес:")
        await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    if not data['weight'].isdigit():
        await message.answer(str_warning)
    else:
        calories_for_male, calories_for_female = calories_calculate(data)
        await message.answer(f"Норма калории для мужчин: {calories_for_male}")
        await message.answer(f"Норма калории для женщин: {calories_for_female}")
        await state.finish()


@dp.message_handler()
async def all_words(message):
    await message.answer('Я бот умеющий расчитывать колории, для начала нажмите /start')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
