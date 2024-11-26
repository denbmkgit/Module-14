from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Стоимость"),
            KeyboardButton(text="О нас")
        ]
    ], resize_keyboard=True
)

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Средняя игра", callback_data="medium")],
        [InlineKeyboardButton(text="Большая игра", callback_data="big")],
        [InlineKeyboardButton(text="Очень большая игра", callback_data="mega")],
        [InlineKeyboardButton(text="Другие предложения", callback_data="other")]
    ]
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Купить!", url="http://ya.ru")],
        [InlineKeyboardButton(text="Назад", callback_data= "back_to_catalog")]
    ]

)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пользователи", callback_data="users")],
        [InlineKeyboardButton(text="Статистика", callback_data="stat")],
        [
         InlineKeyboardButton(text="Блокировка", callback_data="block"),
         InlineKeyboardButton(text="разблокировка", callback_data="unblock")
        ]
    ]
)

product_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
         InlineKeyboardButton(text="Product1", callback_data="product_buying"),
         InlineKeyboardButton(text="Product2", callback_data="product_buying"),
         InlineKeyboardButton(text="Product3", callback_data="product_buying"),
         InlineKeyboardButton(text="Product4", callback_data="product_buying"),
        ]
    ]
)
