from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from main import dp, bot
from keyboards import (start_button,
                       go_button,
                       filter_button,
                       get_button_list,
                       send_message_button)
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

    scrapper.login(login_details["login"], login_details["password"])
    scrapper.search_in()

    await msg.answer("Отлично! Вход выполнен, можем продолжать"
                     "Вы можете выбрать фильтры сферы деятельности"
                     "и должности людей которым будем делать рассылку",
                     reply_markup=go_button)


@dp.message_handler(Text(equals=["Поехали", "Ok"]))
async def filter_by(msg: types.Message):
    await msg.answer("Выберите фильтр", reply_markup=filter_button)


@dp.message_handler(Text(equals="Деятельность"))
async def filter_by_industry(msg: types.Message):
    scrapper.click_to_industry()
    lst = scrapper.get_industry_list()
    await msg.answer("Выберите фильтр", reply_markup=get_button_list(lst))


@dp.message_handler(Text(equals="Должность"))
async def filter_by_function(msg: types.Message):
    scrapper.click_to_functions()
    lst = scrapper.get_functions_list()
    await msg.answer("Выберите фильтр", reply_markup=get_button_list(lst))


@dp.message_handler(Text(equals="Поиск"))
async def done(msg: types.Message):
    scrapper.search()
    # scrapper.get_count_users()
    await msg.answer("Найдено количество", reply_markup=send_message_button)


