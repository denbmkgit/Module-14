from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()

button5 = KeyboardButton(text='Купить')

button1 = KeyboardButton(text='Расчитать')
button2 = KeyboardButton(text="Информация")
kb.row(button1, button2)
kb.add(button5)


kb_in_line = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Расчитать норму колорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb_in_line.add(button3)
kb_in_line.add(button4)

kb_in_line_buy = InlineKeyboardMarkup(
    keyword=[
        [
        InlineKeyboardButton(text='Product1'),
        InlineKeyboardButton(text='Product2'),
        InlineKeyboardButton(text='Product3'),
        InlineKeyboardButton(text='Product4'),
        ]
    ], resize_keybord=True)


kb_in_line_buy= InlineKeyboardMarkup(resize_keyboard=True)
inl_button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
inl_button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
inl_button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
inl_button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_in_line_buy.row(inl_button1, inl_button2, inl_button3, inl_button4)


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(1,5):
        with open(f'files/{i}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: Product{i} | Описание: Описание{i} | Цена: {i * 100}')
    with open('files/M.png', 'rb') as img:
        await message.answer_photo(img, 'Выберете продукт для покупки:',reply_markup=kb_in_line_buy)


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in_line)


@dp.callback_query_handler(text='formulas')
async def  get_formulas(call):
    await call.message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: '
                              'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5,  '
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


str_warning = "Задавайте только целые числа"


def calories_calculate(data):
    calories_for_male = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) + 5
    calories_for_female = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 5 * int(data['age']) - 161
    return calories_for_male, calories_for_female


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer('Привет! Я бот умеющий расчитать колории для тебя.', reply_markup=kb)


@dp.message_handler(text=["Информация"])
async def information(message):
    await message.answer("Я бот помогающий твоему здоровью, расчитывая необходимую для тебя норму потребления колорий "
                         "используя упрощённую формулу Миффлина - Сан Жеора", reply_markup=kb)


@dp.callback_query_handler(text=['product_buying'])
async def end_confirm_message(call):
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
