from aiogram.dispatcher.filters.state import StatesGroup, State


class LogInLinkedinStates(StatesGroup):
    write_login = State()
    write_password = State()


class OneCompanyProfileStates(StatesGroup):
    paste_one_company_profile = State()
    write_subject_message = State()
    write_text_message = State()
    confirm_or_cancel = State()