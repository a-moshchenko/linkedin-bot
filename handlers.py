from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from main import dp
from keyboards import *
from FSM import *
from database import *
from search_users import check_users_from_sales_navigator_form


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
                     "Вы хотите вставить профиль только одной компании или отправить файлом целый список? "
                     "В случае если данные введены не верно, их можно изменить.",
                     reply_markup=one_company_or_file)


# при необходимости изменить данные для входа
@dp.message_handler(Text(equals="Изменить данные"))
async def change_login_details(msg: types.Message):
    await clear_all_data_in_login_details()  # очищаем таблицу с данными для входа

    await msg.answer("Данные очищены. Нажмите на кнопку для продолжения",
                     reply_markup=start_button)


# !!!!!!!! НАЧАЛО СЦЕНАРИЯ С РАССЫЛКОЙ ДЛЯ ОДНОЙ КОМПАНИИ !!!!!!!!

# если нужно вставить профиль одной компании
@dp.message_handler(Text(equals="Одну компанию"))
async def paste_one_company_profile_link(msg: types.Message):
    await msg.answer("Вставьте ссылку на профиль комнании на LinkedIn.",
                     reply_markup=ReplyKeyboardRemove())

    await OneCompanyProfileStates.paste_one_company_profile.set()


# получаем тему(заголовок) сообщения
@dp.message_handler(state=OneCompanyProfileStates.paste_one_company_profile)
async def write_subject_message(msg: types.Message, state: FSMContext):
    await state.update_data(
        {"profile_link": msg.text}
    )

    await msg.answer("Введите тему (заголовок) вашего сообщения.")

    await OneCompanyProfileStates.write_subject_message.set()


# получаем сам текст сообщения
@dp.message_handler(state=OneCompanyProfileStates.write_subject_message)
async def write_text_message(msg: types.Message, state: FSMContext):
    await state.update_data(
        {"subject_msg": msg.text}
    )

    await msg.answer("Введите текст вашего сообщения.")

    await OneCompanyProfileStates.write_text_message.set()


# спрашиваем подтверждение на рассылку
@dp.message_handler(state=OneCompanyProfileStates.write_text_message)
async def confirm_mailing(msg: types.Message, state: FSMContext):
    await state.update_data(
        {"text_msg": msg.text}
    )

    mailing_data = await state.get_data()

    await msg.answer("Вот данные, которые вы ввели.\n"
                     f"<b>Профиль компании:</b> {mailing_data['profile_link']}\n"
                     f"<b>Тема сообщения:</b> {mailing_data['subject_msg']}\n"
                     f"<b>Текст:</b>\n{mailing_data['text_msg']}\n"
                     "Подтвердите, либо отмените рассылку.",
                     reply_markup=confirm_or_cancel_mailing)

    await OneCompanyProfileStates.confirm_or_cancel.set()


# отмена рассылки
@dp.message_handler(Text(equals="Отменить"), state=OneCompanyProfileStates.confirm_or_cancel)
async def cancel_mailing(msg: types.Message, state: FSMContext):
    await clear_all_data_in_login_details()  # очищаем таблицу с данными для входа

    await msg.answer("Рассылка отменена. Нажмите кнопку, чтобы начать новую.",
                     reply_markup=start_button)

    await state.finish()


# если рассылка подтверждена
@dp.message_handler(Text(equals="Подтвердить"), state=OneCompanyProfileStates.confirm_or_cancel)
async def confirm_mailing(msg: types.Message, state: FSMContext):
    message_data = await state.get_data()

    await write_message_data_in_table(message_data['profile_link'], message_data['subject_msg'],
                                      message_data['text_msg'])

    await msg.answer("Рассылка подтверждена и начинается.")

    await check_users_from_sales_navigator_form()

# !!!!!!!! КОНЕЦ СЦЕНАРИЯ С РАССЫЛКОЙ ДЛЯ ОДНОЙ КОМПАНИИ !!!!!!!!
