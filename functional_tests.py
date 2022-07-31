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
            service=Service(GeckoDriverManager().install()), options=options
        )
        self.browser.implicitly_wait(30)
        # self.browser.maximize_window()

    def tearDown(self):
        self.browser.quit()

    # def test_can_start_app(self):
    #     response = self.browser.get(f"{self.BASE_URL}")

    #     # user sees website title as tab title
    #     self.assertIn("Golden - Home", self.browser.title)

    #     # user sees different data lists
    #     data_list = [
    #         "product-categories",
    #         "showrooms",
    #         "stores",
    #         "products",
    #         "new-arrivals",
    #     ]

    #     for data_list_name in data_list:
    #         self.browser.find_element(
    #             By.CSS_SELECTOR, f'ul[data-context="{data_list_name}"]'
    #         )

    # def test_user_click_product_tab(self):
    #     # user is at home page
    #     response = self.browser.get(f"{self.BASE_URL}/")

    #     # the user see the "product" tab and decides to click on it
    #     product_tab = self.browser.find_element(
    #         By.CSS_SELECTOR, f'a[data-link="products"]'
    #     )
    #     product_tab.click()

    # def test_user_select_single_product(self):
    #     # user is at home page
    #     response = self.browser.get(f"{self.BASE_URL}/")

    #     # the user see an interesting product and decides to click on it
    #     product_list = self.browser.find_element(
    #         By.CSS_SELECTOR, f'ul[data-context="products"]'
    #     )

    #     # selecting first item in list
    #     selected_item = self.browser.find_element(By.CSS_SELECTOR, 'li[data-product-index="1"] a')
    #     selected_item_name = selected_item.find_element(By.CSS_SELECTOR, 'span').text
    #     selected_item.click()

    #     # user sees detail page with product that he selected
    #     product_name = self.browser.find_element(By.ID, 'product-name').text
    #     self.assertEqual(product_name, selected_item_name)

    def test_user_selects_category(self):
        # at home page
        # user is at home page
        response = self.browser.get(f"{self.BASE_URL}/")

        # the user see the "categories" and decides to click on the first category
        selected_category = self.browser.find_element(
            By.CSS_SELECTOR, 'li[data-category-index="1"] a'
        )
        selected_category_name = selected_category.find_element(By.CSS_SELECTOR, 'span').text

        selected_category.click()

        # use sees selected category name as tab title and page title
        self.assertIn(f"Golden - {selected_category_name}", self.browser.title)

        category_name = self.browser.find_element(By.ID, 'category-name').text

        self.assertEqual(selected_category_name, category_name)


if __name__ == "__main__":
    unittest.main()
