import requests
from selenium import webdriver
import json
import time

from database import *
from main import bot
from keyboards import start_button


class Scraper:
    """Подключается к LinkedIn и собирает
    """
    def __init__(self):
        self.username = select_login()
        self.password = select_password()
        self.browser = webdriver.Chrome(executable_path='./chromedriver')

    def login(self):
        """CONNECTS TO LINKEDIN
        """
        self.browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        time.sleep(3)

        # вводим логин и пароль
        elementID = self.browser.find_element_by_id("username")
        elementID.send_keys(self.username)
        time.sleep(2)

        elementID = self.browser.find_element_by_id("password")
        elementID.send_keys(self.password)
        time.sleep(1)

        elementID.submit()

    def search_in(self):  # входим в поиск по фильтру и устанавливаем фильтр местоположения Ukraine
        self.browser.get("https://www.linkedin.com/sales/search/people")
        time.sleep(15)
        self.browser.find_element_by_xpath('/html/body/div[5]/header/div/div[3]/section/div/div/div[1]/div/div/div[1]/a').click()
        time.sleep(5)

        # жмем на фильтр по местоположению
        geografy_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[1]/div/button"
        self.browser.find_element_by_xpath(geografy_filter_xpath).click()
        time.sleep(3)

        # вводим название страны
        geografy_filter_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[2]/input"
        self.browser.find_element_by_xpath(geografy_filter_input_xpath).send_keys('Ukraine')
        time.sleep(2)

        # выбираем локаль Украина
        needed_company_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[2]/ol/li[1]/button"
        self.browser.find_element_by_xpath(needed_company_link_xpath).click()
        time.sleep(3)

    def click_to_industry(self):  # жмем на фильтр по сфере деятельности
        industry_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[1]/div/button"
        self.browser.find_element_by_xpath(industry_filter_xpath).click()
        time.sleep(2)

    def input_industry(self, industries):  # вводим название сферы деятельности
        for i in industries:
            industry_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/input"
            self.browser.find_element_by_xpath(industry_input_xpath).send_keys(f'{i}')
            time.sleep(2)

            # выбираем сферу деятельности
            industry_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li[1]/button"
            self.browser.find_element_by_xpath(industry_link_xpath).click()
            time.sleep(2)

    def click_to_functions(self):  # жмем на фильтр по должности
        function_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[1]/div/button"
        self.browser.find_element_by_xpath(function_filter_xpath).click()
        time.sleep(2)

    def input_functions(self, functions):  # вводим название должностей
        for i in functions:
            functions_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/input"
            self.browser.find_element_by_xpath(functions_input_xpath).send_keys(f'{i}')
            time.sleep(2)

            # выбираем должности
            industry_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li[1]/button"
            self.browser.find_element_by_xpath(industry_link_xpath).click()
            time.sleep(2)

    def search(self):  # жмем на кнопку 'поиск'
        search_btn_xpath = "/html/body/div[3]/div/div/div[1]/div[2]/button"
        self.browser.find_element_by_xpath(search_btn_xpath).click()

    def get_industry_list(self):  # собирает список всех сфер деятельности для выбора в bot
        industries = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li/button')]
        return industries

    def get_functions_list(self):  # собирает список всех должностей для выбора в bot
        functions = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li/button')]
        return functions

    def get_search_pages(self):  # парсим количество страниц после поиска
        pages = [i.text for i in self.browser.find_elements_by_xpath('/html/body/main/div[1]/div/section/div[2]/nav/ol/li/button')]
        return pages[-1]

    def get_userlist(self, pages):  # возвращает список найденых пользователей
        page_list = {}
        for i in range(1, int(pages) - 98):
            current_scroll_position, new_height = 0, 1
            while current_scroll_position <= new_height:  # прокрутка в конец страницы
                current_scroll_position += 10
                self.browser.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                new_height = self.browser.execute_script("return document.body.scrollHeight")
            user = {i.text: i.get_attribute('href') for i in self.browser.find_elements_by_xpath('/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li/div[2]/div/div/div/article/section[1]/div[1]/div/dl/dt/a')}
            page_list.update(user)
            self.browser.find_element_by_xpath('/html/body/main/div[1]/div/section/div[2]/nav/button[2]/span').click()
        return page_list

    def send_message(self, user_list, message):  # рассылка сообщений
        for name, link in user_list.items():
            user_name = name
            user_link = link
            self.browser.get(user_link)
            time.sleep(2)
            self.browser.find_element_by_xpath('/html/body/main/div[1]/div[2]/div/div[2]/div[1]/div[2]/button').click()
            time.sleep(2)
            input_subject_xpath = '/html/body/div[6]/section/div[2]/section/div[2]/form[1]/input'
            textarea_message_xpath = '/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[1]/textarea'
            self.browser.find_element_by_xpath(input_subject_xpath).send_keys(f'Добрий день! {name}')
            time.sleep(1)
            self.browser.find_element_by_xpath(textarea_message_xpath).send_keys(message)
            time.sleep(2)
            self.browser.find_element_by_xpath('/html/body/div[6]/section/div[2]/section/div[2]/form[1]/section[2]/span/button').click()
            time.sleep(15)


if __name__ == '__main__':
    message = '''Добрий день!Я - бот, який збирає HR для автоматизованого рiшення
                 проблем вигорання IT-фахівців i iх утримання. Крім того, це вирішення
                 допоможе більш ефективно вибудувати процес рекрутингу за допомого експертної
                 системи, яка має можливість машинного навчання з боку користувача.'''
    scraper = Scraper()
    scraper.login()
    time.sleep(30)
    scraper.search_in()
    scraper.click_to_industry()
    scraper.input_industry(scraper.get_industry_list()[:4:])
    scraper.click_to_functions()
    scraper.input_functions(scraper.get_functions_list()[:2:])
    scraper.search()
    time.sleep(5)
    page = scraper.get_search_pages()
    userlist = scraper.get_userlist(page)
    time.sleep(7)
    scraper.send_message(userlist, message)
