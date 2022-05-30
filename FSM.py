from aiogram.dispatcher.filters.state import StatesGroup, State


class LogInLinkedinStates(StatesGroup):
    write_login = State()
    write_password = State()


class MessageStates(StatesGroup):
    write_subject = State()
    write_body = State()
