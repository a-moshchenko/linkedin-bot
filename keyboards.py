from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Начать")
        ]
    ],
    resize_keyboard=True
)

filter = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Сфера"),
            KeyboardButton("Должность")
        ],
        [
            KeyboardButton("Поехали!!")
        ],
        [
            KeyboardButton("Изменить данные")
        ]
    ],
    resize_keyboard=True
)
