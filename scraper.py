from selenium import webdriver
import time
import json

from selenium.common.exceptions import NoSuchElementException

from config import DEBUG

from main import bot

from database import Message, get_all, Customer, create_customer


async def send_message_to_bot(msg):
    await bot.send_message(msg)


class Scraper:
    """Подключается к LinkedIn и собирает
    """

    stop = False

    def __init__(self):
        options = webdriver.ChromeOptions()
        if DEBUG:
            options.headless = False
        else:
            options.headless = True
        self.browser = webdriver.Chrome(executable_path='./chromedriver', options=options)


    def login(self, username, password):
        """CONNECTS TO LINKEDIN
        """

        self.browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        time.sleep(1)

        # вводим логин и пароль
        elementID = self.browser.find_element_by_id("username")
        elementID.send_keys(username)

        elementID = self.browser.find_element_by_id("password")
        elementID.send_keys(password)

        elementID.submit()
        time.sleep(7)

    def search_in(self):  # входим в поиск по фильтру и устанавливаем фильтр местоположения Ukraine
        self.browser.get("https://www.linkedin.com/sales/search/people")
        time.sleep(7)

        all = '//*[@id="ember44"]'
        element = self.browser.find_element_by_xpath(all)
        # self.browser.execute_script("arguments[0].click();", element)
        webdriver.ActionChains(self.browser).move_to_element(element).click(element).perform()

        time.sleep(3)

        # жмем на фильтр по местоположению
        geo_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[1]/div/button"
        geo = self.browser.find_element_by_xpath(geo_filter_xpath)
        time.sleep(1)
        webdriver.ActionChains(self.browser).move_to_element(geo).click(geo).perform()
        time.sleep(2)

        # вводим название страны
        country_filter_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[2]/input"
        self.browser.find_element_by_xpath(country_filter_input_xpath).send_keys('Ukraine')
        time.sleep(2)

        # выбираем локаль Украина
        needed_company_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[2]/ol/li[1]/button"
        get_country = self.browser.find_element_by_xpath(needed_company_link_xpath)
        webdriver.ActionChains(self.browser).move_to_element(get_country).click(get_country).perform()

    def click_to_industry(self):  # жмем на фильтр по сфере деятельности
        industry_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[1]/div/button"
        ind = self.browser.find_element_by_xpath(industry_filter_xpath)
        webdriver.ActionChains(self.browser).move_to_element(ind).click(ind).perform()

    def input_industry(self, industries):  # вводим название сферы деятельности
        for i in industries:
            industry_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/input"
            self.browser.find_element_by_xpath(industry_input_xpath).send_keys(f'{i}')
            time.sleep(1.5)

            # выбираем сферу деятельности
            industry_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li[1]/button"
            industry_x = self.browser.find_element_by_xpath(industry_link_xpath)
            webdriver.ActionChains(self.browser).move_to_element(industry_x).click(industry_x).perform()

    def click_to_functions(self):  # жмем на фильтр по должности
        function_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[1]/div/button"
        func = self.browser.find_element_by_xpath(function_filter_xpath)
        webdriver.ActionChains(self.browser).move_to_element(func).click(func).perform()

    def input_functions(self, functions):  # вводим название должностей
        for i in functions:
            functions_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/input"
            self.browser.find_element_by_xpath(functions_input_xpath).send_keys(f'{i}')
            time.sleep(1)

            # выбираем должности
            industry_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li[1]/button"
            func_x = self.browser.find_element_by_xpath(industry_link_xpath)
            webdriver.ActionChains(self.browser).move_to_element(func_x).click(func_x).perform()

    def search(self):  # жмем на кнопку 'поиск'
        search_btn_xpath = "/html/body/div[3]/div/div/div[1]/div[2]/button"

        search_x = self.browser.find_element_by_xpath(search_btn_xpath)
        webdriver.ActionChains(self.browser).move_to_element(search_x).click(search_x).perform()

        time.sleep(2)

    def get_industry_list(self):  # собирает список всех сфер деятельности для выбора в bot
        try:
            industries = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li/button')]
        except NoSuchElementException:

            industries = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[8]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li/button')]
        return industries

    def get_functions_list(self):  # собирает список всех должностей для выбора в bot
        try:
            functions = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li/button')]
        except NoSuchElementException:
            functions = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[8]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li/button')]
        return functions

    def get_search_pages(self):  # парсим количество страниц после поиска
        pages = [i.text for i in self.browser.find_elements_by_xpath('/html/body/main/div[1]/div/section/div[2]/nav/ol/li/button')]
        return int(pages[-1])

    def check_status(self, n):  # проверяем сохранен ли контакт у нас
        try:
            xpath = f'/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{n}]/div[2]/div/div/div/article/section[1]/div[1]/div/dl/dd[1]/ul/li[3]'
            if self.browser.find_element_by_xpath(xpath).text == 'Saved':
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    def get_customer(self):
        customer = self.browser.find_element_by_xpath('/html/body/main/div[1]/div[2]/div/div[1]/div[1]/div/dl/dt/span')
        return customer.text

    def send_message(self):  # отправка сообщения
        open_message = '/html/body/main/div[1]/div[2]/div/div[2]/div[1]/div[2]/button'  # открываем окно ввода сообщения
        send = self.browser.find_element_by_xpath(open_message)
        webdriver.ActionChains(self.browser).move_to_element(send).click(send).perform()

        time.sleep(5)

        message = get_all(Message)[0]  # достаем сообщение из БД

        # вводим тему
        try:
            try:
                input_subject_xpath = '/html/body/div[6]/section/div[2]/section/div[2]/form[1]/input'
            except NoSuchElementException:
                input_subject_xpath = '/html/body/div[4]/section/div[2]/section/div[2]/form[1]/input'
            self.browser.find_element_by_xpath(input_subject_xpath).send_keys(message.subject)
        except NoSuchElementException:
            print('тема уже есть')
        time.sleep(1)

        # вводим сообщение
        input_body_xpath = '/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[1]/textarea'
        self.browser.find_element_by_xpath(input_body_xpath).send_keys(message.body)
        time.sleep(1)
        if not DEBUG:  # если DEBUG==False отправляем сообщения
            send_button_xpath = '/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[2]/span/button'
            self.browser.find_element_by_xpath(send_button_xpath).click()
            print('message.send')
        elif DEBUG:  # если DEBUG==True закрываем окно ввода
            time.sleep(2)
            try:
                close_message = self.browser.find_element_by_xpath('/html/body/div[4]/section/header/button[2]')
            except NoSuchElementException:

                close_message = self.browser.find_element_by_xpath('/html/body/div[6]/section/header/button[2]')
            self.browser.execute_script("(arguments[0]).click();", close_message)
            time.sleep(2)
            try:
                close = self.browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]')
            except NoSuchElementException:
                close = self.browser.find_element_by_xpath('/html/body/div[10]/div/div/div[3]/button[2]')
            self.browser.execute_script("(arguments[0]).click();", close)

    def next_page(self):
        # нажимаем next для перехода на следующую страницу
        next = self.browser.find_element_by_xpath('/html/body/main/div[1]/div/section/div[2]/nav/button[2]')
        self.browser.execute_script("(arguments[0]).click();", next)

    def open_user_page(self, num):  # переходит на страницу пользователя
        username_link_xpath = f'/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{num}]/div[2]/div/div/div/article/section[1]/div[1]/div/dl/dt/a'
        time.sleep(2)
        window = self.browser.find_element_by_xpath(username_link_xpath)
        self.browser.execute_script("(arguments[0]).click();", window)

    def go_back(self):  # возвращает на предыдущую страницу
        self.browser.back()

    def scroll(self):  # прокручивает всю страницу, чтобы загрузить все элементы
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:  # прокрутка в конец страницы
            current_scroll_position += 150
            self.browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.browser.execute_script("return document.body.scrollHeight")

    def click_to_show_all_info(self):
        count_xpath = '/html/body/main/div[1]/div[2]/div/div[2]/div[3]/dl/dd'
        count = self.browser.find_elements_by_xpath(count_xpath)

        show_xpath = f'/html/body/main/div[1]/div[2]/div/div[2]/div[3]/dl/dd[{len(count)}]/button'
        show = self.browser.find_element_by_xpath(show_xpath)

        self.browser.execute_script("(arguments[0]).click();", show)

    def click_to_hide_all_info(self):
        try:
            hide_xpath = '/html/body/div[3]/div/div/button'
            hide = self.browser.find_element_by_xpath(hide_xpath)
        except NoSuchElementException:
            hide_xpath = '/html/body/div[8]/div/div/button'
            hide = self.browser.find_element_by_xpath(hide_xpath)

        self.browser.execute_script("(arguments[0]).click();", hide)

    def get_profile_url(self, num):
        url_xpath = f'/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{num}]/div[2]/div/div/div/article/section[1]/div[1]/div/dl/dt/a'
        url = self.browser.find_element_by_xpath(url_xpath).get_attribute('href')
        return url

    def check_email(self):
        try:
            try:
                email_xpath = '/html/body/div[3]/div/div/div[2]/div/section[2]/div/div[1]/a'
            except NoSuchElementException:

                email_xpath = '/html/body/div[8]/div/div/div[2]/div/section[2]/div/div[1]/a'
            email_element = self.browser.find_element_by_xpath(email_xpath)
            return email_element.text
        except NoSuchElementException:
            return None
