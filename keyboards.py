from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Начать")
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
            KeyboardButton("Деятельность")
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
    my_buttons["keyboard"].append([{"text": "Ok"}])
            
    return my_buttons
