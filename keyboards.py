from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Начать")
        ]
    ],
    resize_keyboard=True
)

one_company_or_file = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Сфера"),
            KeyboardButton("Должность")
        ],
        [
            KeyboardButton("Изменить данные")
        ],
        [
            KeyboardButton("Поехали!!")
        ]
    ],
    resize_keyboard=True
)

confirm_or_cancel_mailing = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Подтвердить"),
            KeyboardButton("Отменить")
        ]
    ],
    resize_keyboard=True
)
