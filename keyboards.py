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
            KeyboardButton("Одну компанию"),
            KeyboardButton("Файл")
        ],
        [
            KeyboardButton("Изменить данные")
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
