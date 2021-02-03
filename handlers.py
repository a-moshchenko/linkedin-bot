import os
import time
import hashlib
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from main import dp, bot
from keyboards import (start_button,
                       go_button,
                       filter_button,
                       get_button_list,
                       message_button,
                       done_button,
                       go_to_message_button,
                       stop_button)
from FSM import LogInLinkedinStates, MessageStates
from database import (create_user,
                      User,
                      Message,
                      Customer,
                      create_message,
                      get_all,
                      create_customer)
from scraper import Scraper

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', )


filter = ''
filter_list = []
scrapper = None
stop = False


def get_hash(password):
    password_salt = os.urandom(32).hex()
    hash = hashlib.sha512()
    hash.update(('%s%s' % (password_salt, password)).encode('utf-8'))
    return hash.hexdigest()


@dp.message_handler(commands=["start"])
async def start_bot(msg: types.Message):
    global scrapper
    scrapper = Scraper()
    await msg.answer("Привет! Я LinkedIn Bot! Буду помогать с рассылкой сообщений. ",
                     reply_markup=start_button)


# вводим логин
@dp.message_handler(Text(equals=["Начать", "Отмена"]))
async def write_login(msg: types.Message):
    await msg.answer("Введите ваш логин на LinkedIn:",
                     reply_markup=ReplyKeyboardRemove())

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
    await msg.answer("Подождите!! Идет авторизация")
    await state.update_data(
        {"password": msg.text}
    )
    login_details = await state.get_data()

    user = msg.from_user

    await state.finish()

    scrapper.login(login_details["login"], login_details["password"])
    time.sleep(5)
    scrapper.search_in()

    create_user(User, id=user['id'], username=user['username'],
                login=login_details["login"],
                password=get_hash(login_details["password"]))
    await msg.answer("Отлично! Вход выполнен, можем продолжать! "
                     "Вы можете выбрать фильтры сферы деятельности "
                     "и должности людей которым будем делать рассылку",
                     reply_markup=go_button)


@dp.message_handler(Text(equals=["Поехали", "Ok"]))
async def filter_by(msg: types.Message):
    global filter
    global filter_list
    if filter == 'industry':
        scrapper.input_industry(set(filter_list))
    elif filter == 'functions':
        scrapper.input_functions(set(filter_list))
    filter = ''
    filter_list = []
    await msg.answer("Выберите", reply_markup=filter_button)


# выбираем сферу деятельности
@dp.message_handler(Text(equals="Сфера деятельности"))
async def filter_by_industry(msg: types.Message, state: FSMContext):
    global filter
    filter = 'industry'
    scrapper.click_to_industry()
    time.sleep(1)
    lst = scrapper.get_industry_list()
    await msg.answer("Выберите (можно несколько) и нажмите 'OK'", reply_markup=get_button_list(lst))


# выбираем должность
@dp.message_handler(Text(equals="Должность"))
async def filter_by_function(msg: types.Message):
    global filter
    filter = 'functions'
    scrapper.click_to_functions()
    time.sleep(1)
    lst = scrapper.get_functions_list()
    await msg.answer("Выберите (можно несколько) и нажмите 'OK'", reply_markup=get_button_list(lst))


# поиск по выбраным критериям
@dp.message_handler(Text(equals="Поиск"))
async def done(msg: types.Message):
    scrapper.search()
    await msg.answer("Поиск закончен", reply_markup=go_to_message_button)


# меню сообщения
@dp.message_handler(Text(equals=["К сообщению", "Готово"]))
async def message_menu(msg: types.Message):
    await msg.answer("Выберите", reply_markup=message_button)


# вводим тему
@dp.message_handler(Text(equals="Изменить сообщение"))
async def write_subject(msg: types.Message):
    await msg.answer("Введите тему сообщения",
                     reply_markup=ReplyKeyboardRemove())

    await MessageStates.write_subject.set()  # FSM.py


# вводим текст
@dp.message_handler(state=MessageStates.write_subject)
async def write_body(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь введите сообщение")

    await state.update_data(
        {"subject": msg.text}
    )
    await MessageStates.write_body.set()


# сохраняем сообщение
@dp.message_handler(state=MessageStates.write_body)
async def save_message(msg: types.Message, state: FSMContext):
    await state.update_data(
        {"body": msg.text}
    )
    message = await state.get_data()

    await state.finish()
    create_message(subject=message['subject'], body=message['body'])
    await msg.answer("Сообщение сохранено!!!", reply_markup=done_button)


@dp.message_handler(Text(equals="Посмотреть сообщение"))
async def view_message(msg: types.Message):
    message = get_all(Message)[0]
    await msg.answer("subject:"
                     f"{message.subject}")
    await msg.answer("body:"
                     f"{message.body}", reply_markup=done_button)


@dp.message_handler(Text(equals="Начать раcсылку"))
async def start_send(msg: types.Message):
    await msg.answer("Рассылка началась", reply_markup=stop_button)
    global scrapper
    try:
        check_list = [i.url for i in get_all(Customer)]
        n = scrapper.get_search_pages()
        time.sleep(3)
        for i in range(n):
            for j in range(1, 26):
                time.sleep(5)
                url = scrapper.get_profile_url(j).split('?')[0]
                if url not in check_list:
                    check_list.append(url)
                    time.sleep(5)
                    scrapper.open_user_page(j)
                    time.sleep(5)
                    customer = scrapper.get_customer()
                    await msg.answer(f"Заходим на страницу {customer}")
                    time.sleep(5)
                    scrapper.click_to_show_all_info()
                    time.sleep(5)
                    email = scrapper.check_email()
                    time.sleep(5)
                    scrapper.click_to_hide_all_info()
                    time.sleep(5)
                    scrapper.send_message()
                    await msg.answer("Сообщение отправлено")
                    time.sleep(5)
                    create_customer(Customer, name=customer, url=url, email=email)
                    time.sleep(5)
                    scrapper.go_back()
                    time.sleep(5)
                    scrapper.scroll()
                else:
                    logging.info("Пользователь сообщение получил")
                    time.sleep(5)
                    scrapper.scroll()
            scrapper.next_page()
    except KeyboardInterrupt as e:
        logging.warning(e)
        scrapper.browser.quit()


@dp.message_handler(Text(equals="Отмена"))
async def stop_send(msg: types.Message):
    exit()
    await msg.answer("Рассылка отменена", reply_markup=start_button)


@dp.message_handler()
async def input_value(msg: types.Message):
    global filter
    if filter:
        global filter_list
        filter_list.append(msg.text)
