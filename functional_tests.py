# django
import os, time
import unittest

# selenium
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class UnAuthenticationUserTest(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = "http://localhost:8000"

        # run with hidden window    
        options = Options()
        options.add_argument("--headless")

        self.browser = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
        self.browser.implicitly_wait(30)
        # self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_app(self):
        response = self.browser.get(f"{self.BASE_URL}")

        # user sees website title as tab title
        self.assertIn("Golden - Home", self.browser.title)

        # user sees different data lists
        data_list = ['product-categories', 'showrooms', 'stores', 'products', 'new-arrivals']

        for data_list_name in data_list:
            self.browser.find_element(By.CSS_SELECTOR, f'ul[data-context="{data_list_name}"]')

    def test_user_click_product_tab(self):
        # user is at home page
        response = self.browser.get(f"{self.BASE_URL}/")

        # the user see the "product" tab and decides to click on it
        product_tab = self.browser.find_element(By.CSS_SELECTOR, f'a[data-link="products"]')
        product_tab.click()

        data_list = ['product-categories', 'products',]

        for data_list_name in data_list:
            self.browser.find_element(By.CSS_SELECTOR, f'ul[data-context="{data_list_name}"]')

    def test_user_select_single_product(self):
        # user is at home page
        response = self.browser.get(f"{self.BASE_URL}/")

        # the user see an interesting product and decides to click on it
        product_list = self.browser.find_element(By.CSS_SELECTOR, f'ul[data-context="products"]')

        # selecting first item in list
        first_item = self.browser.find_elements(By.CSS_SELECTOR, 'ul[data-context="products"] li')[0]
        first_item.click()
        


if __name__ == "__main__":
    unittest.main()
