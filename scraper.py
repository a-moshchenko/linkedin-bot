import requests
from selenium import webdriver
import json
import time
import tqdm

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

        #Enter login info:
        elementID = self.browser.find_element_by_id('username')
        elementID.send_keys(self.username)
        time.sleep(2)

        elementID = self.browser.find_element_by_id('password')
        elementID.send_keys(self.password)
        time.sleep(1)

        elementID.submit()

    def search_people(self):
        self.browser.get("https://www.linkedin.com/sales/search/people")
        time.sleep(15)
        self.browser.find_element_by_id('ember44').click()
        time.sleep(15)
        company_filter_xpath = "//div/a[@class='ember-view global-typeahead-container__all-filters-link global-typeahead__input-addon-button display-flex artdeco-button artdeco-button--1 artdeco-button--muted artdeco-button--tertiary full-heigh']"
        self.browser.find_element_by_xpath(company_filter_xpath).click()
        but = '//ul[@class="advanced-search-filter__list"]/li[2]/button'
        self.browser.find_element_by_xpath(but).click()


if __name__ == '__main__':
    scraper = Scraper()
    scraper.login()
    scraper.search_people()
