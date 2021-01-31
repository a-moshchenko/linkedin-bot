from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Начать")
        ]
    ],
    resize_keyboard=True
)

stop_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Отмена")
        ]
    ],
    resize_keyboard=True
)

go_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Поехали")
        ],
    ],
    resize_keyboard=True
)

filter_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Сфера деятельности")
        ],
        [
            KeyboardButton("Должность")
        ],
        [
            KeyboardButton("Поиск")
        ]
    ],
    resize_keyboard=True
)


def get_button_list(lst):
    my_buttons = ReplyKeyboardMarkup(
       keyboard=[
           [
            KeyboardButton(f"{i}")
           ] for i in lst
       ]
    )
    my_buttons.add("Ok")

    return my_buttons


message_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Посмотреть сообщение")
        ],
        [
            KeyboardButton("Изменить сообщение")
        ],
        [
            KeyboardButton("Начать раcсылку")
        ]
    ],
    resize_keyboard=True
)


done_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Готово")
        ],
        [
            KeyboardButton("Начать раcсылку")
        ],
    ],
    resize_keyboard=True
)

go_to_message_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("К сообщению")
        ],
    ],
    resize_keyboard=True
)
