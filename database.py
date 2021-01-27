import sqlite3

conn = sqlite3.connect("linkedin_bot_data.db")
cur = conn.cursor()


# сохранение данных для входа в аккаунт
async def save_login_details_in_db(login, password):
    cur.execute("""INSERT INTO login_details (login, password) VALUES (?, ?)""", (login, password))
    conn.commit()


# получение логина из таблицы
def select_login():
    cur.execute("""SELECT login FROM login_details""")
    login_db = cur.fetchone()

    return login_db[0]


# получение пароля из таблицы
def select_password():
    cur.execute("""SELECT password FROM login_details""")
    password_db = cur.fetchone()

    return password_db[0]


# полностью очищаем таблицу с данными для входа
async def clear_all_data_in_login_details():
    cur.execute("""DELETE FROM login_details""")
    conn.commit()


# ввод данных сообщения в таблицу
async def write_message_data_in_table(profile, subject, text):
    cur.execute("""INSERT INTO message_data (company, subject, msg_text) VALUES (?, ?, ?)""", (profile, subject, text))
    conn.commit()


# получаем ссылку на профиль компании
def get_company_url():
    cur.execute("""SELECT company FROM message_data""")
    company_db = cur.fetchone()

    return company_db[0]


# получаем тему сообщения
def select_subject_message():
    cur.execute("""SELECT subject FROM message_data""")
    subject_db = cur.fetchone()

    return subject_db[0]


# получаем текст сообщения
def select_text_message():
    cur.execute("""SELECT msg_text FROM message_data""")
    msg_text_db = cur.fetchone()

    return msg_text_db[0]


# получаем user_id
async def get_user_id_from_db():
    cur.execute("""SELECT user_id FROM login_details""")
    user_id = cur.fetchone()

    return user_id[0]


# чистим все таблицы в БД
async def clear_all_tables_in_db():
    cur.execute("""DELETE FROM login_details""")
    conn.commit()

    cur.execute("""DELETE FROM message_data""")
    conn.commit()
