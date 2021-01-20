from selenium import webdriver
import time
import math

from database import *

browser = webdriver.Chrome()  # создаем объект Chrome браузера


# запуск процесса рассылки сообщений
async def send_messages_for_users(count_users):
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
                pass
            else:
                username_link_xpath = f"/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{j+1}]/div[2]/div/div" \
                                      f"/div/article/section[1]/div[1]/div/dl/dt/a"
                browser.find_element_by_xpath(username_link_xpath).click()

                time.sleep(6)

                send_msg_btn_xpath = "/html/body/main/div[1]/div[2]/div/div[2]/div[1]/div[2]/button"
                browser.find_element_by_xpath(send_msg_btn_xpath).click()

                time.sleep(6)

                subject_text = select_subject_message()
                text_msg = select_text_message()

                subject_msg_xpath = "/html/body/div[6]/section/div[2]/section/div[2]/form[1]/input"
                browser.find_element_by_xpath(subject_msg_xpath).send_keys(subject_text)

                time.sleep(6)

                text_message_xpath = "/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[1]/textarea"
                browser.find_element_by_xpath(text_message_xpath).send_keys(text_msg)

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
                break


# вход в аккаунт и подсчет количества работников, удовлетворяющих условию
async def check_users_from_sales_navigator_form():
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

    # получаем название компании
    company_link = get_company_url()
    browser.get(company_link)  # посредством метода get, переходим по указаному URL

    time.sleep(15)

    company_name_xpath = "/html/body/div[7]/div[3]/div/div[3]/div[1]/section/div/div/div[2]/div[1]/div[1]/div[2]/div/h1/span"
    company_name = browser.find_element_by_xpath(company_name_xpath).get_attribute("textContent")

    browser.get("https://www.linkedin.com/sales/search/people")  # переходим в sales navigator

    time.sleep(15)   # пауза 15 сек для полной прогрузки страницы

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

    # !!!!! ЗАПУСК ПРОЦЕССА РАССЫЛКИ СООБЩЕНИЯ !!!!!
    await send_messages_for_users(people_accounts)
