from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from main import dp, bot
from keyboards import start_button, filter
from FSM import LogInLinkedinStates
from database import save_login_details_in_db
from scraper import Scraper


scrapper = Scraper()


@dp.message_handler(commands=["start"])
async def start_bot(msg: types.Message):
    await msg.answer("Привет! Я LinkedIn Bot! Буду помогать с рассылкой сообщений. ",
                     reply_markup=start_button)


# вводим логин
@dp.message_handler(Text(equals="Начать"))
async def write_login(msg: types.Message):
    await msg.answer("Введите ваш логин на LinkedIn:", reply_markup=ReplyKeyboardRemove())

    await LogInLinkedinStates.write_login.set()  # FSM.py


# вводим пароль
@dp.message_handler(state=LogInLinkedinStates.write_login)
async def write_password(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь введите ваш пароль:")

    await state.update_data(
        {"login": msg.text}
    )
    await LogInLinkedinStates.write_password.set()


# сохраняем логин и пароль
@dp.message_handler(state=LogInLinkedinStates.write_password)
async def save_login_and_password(msg: types.Message, state: FSMContext):
    await state.update_data(
        {"password": msg.text}
    )

    login_details = await state.get_data()

    await save_login_details_in_db(login_details["login"], login_details["password"])

    await state.finish()

    await msg.answer("Отлично! Вот данные, которые вы ввели:\n"
                     f"Логин: {login_details['login']}\n"
                     f"Пароль: {login_details['password']}\n"
                     "Вы можете выбрать фильтры сферы деятельности"
                     "и должности людей которым будем делать рассылку"
                     "В случае если данные введены не верно, их можно изменить.",
                     reply_markup=filter)
