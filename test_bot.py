"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text


API_TOKEN = '1660399463:AAFiWrbwQJz3OqUFi_NsC-PXRLRivqkuLxw'

filter = 2

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Начать")
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


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup=start_button)


# выбираем должность
@dp.message_handler(Text(equals="Начать"))
async def filter_by_function(msg: types.Message):
    global filter
    filter = 1
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    await msg.answer("Выберите фильтр", reply_markup=get_button_list(lst))


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    global filter
    if filter == 1:
        print(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
