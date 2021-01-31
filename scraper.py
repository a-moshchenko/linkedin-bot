from selenium import webdriver
import time

from selenium.common.exceptions import NoSuchElementException

from config import DEBUG

from main import bot

from database import Message, get_all, check_in_db, Customer


async def send_message_to_bot(msg):
    await bot.send_message(msg)


class Scraper:
    """Подключается к LinkedIn и собирает
    """
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
        time.sleep(25)

    def search_in(self):  # входим в поиск по фильтру и устанавливаем фильтр местоположения Ukraine
        self.browser.get("https://www.linkedin.com/sales/search/people")
        time.sleep(5)
        self.browser.find_element_by_xpath('/html/body/div[5]/header/div/div[3]/section/div/div/div[1]/div/div/div[1]/a').click()
        time.sleep(1)

        # жмем на фильтр по местоположению
        geo_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[1]/div/button"
        self.browser.find_element_by_xpath(geo_filter_xpath).click()
        time.sleep(2)

        # вводим название страны
        country_filter_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[2]/input"
        self.browser.find_element_by_xpath(country_filter_input_xpath).send_keys('Ukraine')
        time.sleep(1)

        # выбираем локаль Украина
        needed_company_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[4]/div/div/div[2]/ol/li[1]/button"
        self.browser.find_element_by_xpath(needed_company_link_xpath).click()

    def click_to_industry(self):  # жмем на фильтр по сфере деятельности
        industry_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[1]/div/button"
        self.browser.find_element_by_xpath(industry_filter_xpath).click()
        time.sleep(2)

    def input_industry(self, industries):  # вводим название сферы деятельности
        for i in industries:
            industry_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/input"
            self.browser.find_element_by_xpath(industry_input_xpath).send_keys(f'{i}')
            time.sleep(1)

            # выбираем сферу деятельности
            industry_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li[1]/button"
            self.browser.find_element_by_xpath(industry_link_xpath).click()

    def click_to_functions(self):  # жмем на фильтр по должности
        function_filter_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[1]/div/button"
        self.browser.find_element_by_xpath(function_filter_xpath).click()
        time.sleep(2)

    def input_functions(self, functions):  # вводим название должностей
        for i in functions:
            functions_input_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/input"
            self.browser.find_element_by_xpath(functions_input_xpath).send_keys(f'{i}')
            time.sleep(1)

            # выбираем должности
            industry_link_xpath = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li[1]/button"
            self.browser.find_element_by_xpath(industry_link_xpath).click()

    def search(self):  # жмем на кнопку 'поиск'
        search_btn_xpath = "/html/body/div[3]/div/div/div[1]/div[2]/button"
        self.browser.find_element_by_xpath(search_btn_xpath).click()
        time.sleep(2)

    def get_industry_list(self):  # собирает список всех сфер деятельности для выбора в bot
        industries = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[1]/ul/li[6]/div/div/div[2]/ol/li/button')]
        return industries

    def get_functions_list(self):  # собирает список всех должностей для выбора в bot
        functions = [i.get_attribute('title').split('  ')[0] for i in self.browser.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[2]/div/section[2]/ul/li[4]/div/div/div[2]/ol/li/button')]
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

    def get_customer(self, num):
        customer = self.browser.find_element_by_xpath(f'/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{num}]/div[2]/div/div/div/article/section[1]/div[1]/div/dl/dt/a')
        return customer.text, customer.get_attribute('href')

    def send_message(self, num):
        xpath_three_dots = f'/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{num}]/div[2]/div/div/div/article/section[1]/div[2]/ul/li/div/div[2]/div/div[1]/button'
        three_dots = self.browser.find_element_by_xpath(xpath_three_dots)
        self.browser.execute_script("$(arguments[0]).click();", three_dots)
        time.sleep(5)

        # открывает окно ввода сообщения
        open_message_window_xpath = f'/html/body/main/div[1]/div/section/div[1]/div/div[1]/ol/li[{num}]/div[2]/div/div/div/article/section[1]/div[2]/ul/li/div/div[2]/div/div[1]/div/div/ul/li[4]'
        open_window = self.browser.find_element_by_xpath(open_message_window_xpath)
        open_window.click()
        # self.browser.execute_script("$(arguments[0]).click();", open_window)
        time.sleep(5)

        message = get_all(Message)[0]  # достаем сообщение из БД

        # вводим тему
        input_subject_xpath = '/html/body/div[6]/section/div[2]/section/div[2]/form[1]/input'
        self.browser.find_element_by_xpath(input_subject_xpath).send_keys(message.subject)

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
            self.browser.find_element_by_xpath('/html/body/div[6]/section/header/button[2]').click()
            time.sleep(2)
            self.browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()

    def next_page():
        # нажимаем next для перехода на следующую страницу
        scraper.browser.find_element_by_xpath('/html/body/main/div[1]/div/section/div[2]/nav/button[2]').click()

    def __del__(self):
        self.browser.close()
        self.browser.quit()
