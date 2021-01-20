from selenium import webdriver
import time
import math

from database import *
from main import bot
from keyboards import start_button

# активация headless режима
option = webdriver.ChromeOptions()
option.headless = True

browser = webdriver.Chrome(options=option)  # создаем объект Chrome браузера, принимаем вышесозданую опцию


# запуск процесса рассылки сообщений
async def send_messages_for_users(count_users):
    user_id = await get_user_id_from_db()
    count = math.ceil(int(count_users) / 25)  # количество страниц
    print("стараницы", count)

    rest = int(count_users) - ((int(count_users) // 25) * 25)  # остаток на последней странице
    print("на последнец странице", rest)

    # цикл рассылки сообщений
    for i in range(count-1):
        for j in range(25):
            time.sleep(10)

            user_profile_block_xpath = f"/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{j+1}]"
            status = browser.find_element_by_xpath(user_profile_block_xpath).get_attribute("data-scroll-into-view")

            # проверяем статус аккаунта, 'открытый' или 'закрытый'
            if "OUT_OF_NETWORK" in status:
                await bot.send_message(user_id, f"У пользователя {j + 1} закрытый профиль")
                pass
            else:
                await bot.send_message(user_id, f"У пользователя {j + 1} открытый профиль")

                username_link_xpath = f"/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{j+1}]/div[2]/div/div" \
                                      f"/div/article/section[1]/div[1]/div/dl/dt/a"
                browser.find_element_by_xpath(username_link_xpath).click()

                await bot.send_message(user_id, "Проведен вход на страницу профиля работника")

                time.sleep(6)

                send_msg_btn_xpath = "/html/body/main/div[1]/div[2]/div/div[2]/div[1]/div[2]/button"
                browser.find_element_by_xpath(send_msg_btn_xpath).click()

                time.sleep(6)

                subject_text = select_subject_message()
                text_msg = select_text_message()

                subject_msg_xpath = "/html/body/div[6]/section/div[2]/section/div[2]/form[1]/input"
                browser.find_element_by_xpath(subject_msg_xpath).send_keys(subject_text)

                await bot.send_message(user_id, "введена тема сообщения")

                time.sleep(6)

                text_message_xpath = "/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[1]/textarea"
                browser.find_element_by_xpath(text_message_xpath).send_keys(text_msg)

                await bot.send_message(user_id, "Введен текст сообщения")

                time.sleep(6)

                send_btn_xpath = "/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[2]/span/button"
                x_btn = browser.find_element_by_xpath(send_btn_xpath)
                print(f"Кнопка {j+1}-", x_btn)

                # time.sleep(1)
                #
                # close_conversation_btn_xpath = "/html/body/div[6]/section/header/button[2]"
                # browser.find_element_by_xpath(close_conversation_btn_xpath).click()
                #
                # browser.back()

                await bot.send_message(user_id, "Тестовый показ завершен, цикл отключается")

                await clear_all_tables_in_db()  # чистим все таблицы в БД

                await bot.send_message(user_id, "Таблицы очищены", reply_markup=start_button)
                break
        browser.quit()
        break


# вход в аккаунт и подсчет количества работников, удовлетворяющих условию
async def check_users_from_sales_navigator_form():
    # получаем user_id для отправки уведомлений
    user_id = await get_user_id_from_db()

    login = select_login()
    password = select_password()

    browser.get("https://www.linkedin.com/")

    # ввоодим логин
    username_xpath = "/html/body/main/section[1]/div[2]/form/div[2]/div[1]/input"
    browser.find_element_by_xpath(username_xpath).send_keys(login)

    # ввоодим пароль
    password_xpath = "/html/body/main/section[1]/div[2]/form/div[2]/div[2]/input"
    browser.find_element_by_xpath(password_xpath).send_keys(password)

    # жмем кнопку 'войти'
    login_in_account_btn_xpath = "/html/body/main/section[1]/div[2]/form/button"
    browser.find_element_by_xpath(login_in_account_btn_xpath).click()

    time.sleep(7)

    await bot.send_message(user_id, f"Прошел вход в аккаунт {login}")

    # получаем название компании
    company_link = get_company_url()
    browser.get(company_link)  # посредством метода get, переходим по указаному URL

    time.sleep(15)

    company_name_xpath = "/html/body/div[7]/div[3]/div/div[3]/div[1]/section/div/div/div[2]/div[1]/div[1]/div[2]/div/h1/span"
    company_name = browser.find_element_by_xpath(company_name_xpath).get_attribute("textContent")

    browser.get("https://www.linkedin.com/sales/search/people")  # переходим в sales navigator

    time.sleep(15)   # пауза 15 сек для полной прогрузки страницы

    await bot.send_message(user_id, "Выполнен вход в sales навигатор")

    # жмем кнопку 'все фильтры'
    all_filters_btn_xpath = "/html/body/div[5]/header/div/div[3]/section/div/div/a"
    browser.find_element_by_xpath(all_filters_btn_xpath).click()

    time.sleep(5)

    # жмем на фильтр по компаниям
    company_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[3]/ul/li[1]/div/div/div[1]/div/button"
    browser.find_element_by_xpath(company_filter_xpath).click()

    time.sleep(2)

    # вводим название компани
    company_name_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[3]/ul/li[1]/div/div/div[2]/input"
    browser.find_element_by_xpath(company_name_input_xpath).send_keys(company_name)

    time.sleep(2)

    await bot.send_message(user_id, f"Введено в фильтр название компании {company_name}")

    # ставим переключатель на 'past'
    past_company_cursor = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[3]/ul/li[1]/div/div/div[3]/div/" \
                          "fieldset/div[2]/label/span"
    browser.find_element_by_xpath(past_company_cursor).click()

    time.sleep(5)

    # выбираем первую компанию по ссылке
    needed_company_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[3]/ul/li[1]/div/div/" \
                                "div[2]/ol/li[1]/button"
    browser.find_element_by_xpath(needed_company_link_xpath).click()

    time.sleep(2)

    # количество найденных аккаунтов
    results_count_xpath = "/html/body/div[3]/div/div/div[1]/div[2]/span/b"
    people_accounts = browser.find_element_by_xpath(results_count_xpath).get_attribute("textContent")

    # жмем на кнопку 'поиск'
    search_btn_xpath = "/html/body/div[3]/div/div/div[1]/div[2]/button"
    browser.find_element_by_xpath(search_btn_xpath).click()

    await bot.send_message(user_id, "Выполнен поиск работников в sales навигатор")

    # !!!!! ЗАПУСК ПРОЦЕССА РАССЫЛКИ СООБЩЕНИЯ !!!!!
    await send_messages_for_users(people_accounts)
