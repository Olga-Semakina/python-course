import operator
import time
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from seleniumpagefactory.Pagefactory import PageFactory


class Cart(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "products_table": ("XPATH", "//*[@class='success']")
    }

    def get_products(self):
        return self.products_table.find_elements(By.XPATH, ".//td")


class Header(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "logout_field": ('ID', 'logout2'),
        "user_field": ('ID', 'nameofuser'),
        "cart_field": ('ID', "cartur")
    }

    def open_cart(self):
        self.cart_field.click_button()
        return Cart(self.driver)


class ProductPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "name_field": ("XPATH", "//*[@class='name']"),
        "price_field": ("XPATH", "//*[@class='price-container']"),
        "add_to_cart_field": ("CSS", "a[onclick='addToCart(10)']")
    }

    def get_price(self):
        price_full = self.price_field.get_text()
        child_text = self.price_field.find_element(By.XPATH, ".//*").get_text()
        return price_full.replace(child_text, "").strip().replace("$", "")

    def add_product_to_cart(self):
        self.add_to_cart_field.click_button()


class LoggedMainPage(PageFactory):
    header: Header

    def __init__(self, driver):
        self.driver = driver
        self.header = Header(self.driver)

    locators = {
        "monitors_field": ('XPATH', "//a[text()='Monitors']"),
        "products_table": ('ID', "tbodyid")
    }

    def open_monitors_list(self):
        self.monitors_field.click_button()
        # couldn't find a way how to detect the Monitors page was loaded
        # as they are practically the same with the home one
        time.sleep(1)

    def get_products_list(self) -> List[WebElement]:
        return self.products_table.find_elements(By.XPATH, ".//div[@class='card-block']")

    def sort_products_desc(self):
        """
        pagination is not taken into account
        """
        products = self.get_products_list()
        product_prices = dict()
        for product in products:
            price = product.find_element(By.XPATH, ".//*[contains(text(),'$')]").text.replace("$", "")
            product_prices.update({product: int(price)})
        products_sorted_desc = dict(sorted(product_prices.items(), key=operator.itemgetter(1), reverse=True))

        return list(products_sorted_desc.keys())

    def open_product_page(self, product: WebElement) -> ProductPage:
        product.find_element(By.XPATH, ".//a").click()
        return ProductPage(self.driver)


class LoginPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "login_field": ('ID', 'loginusername'),
        "password_field": ('ID', 'loginpassword'),
        "signin_button": ('XPATH', '//button[text()="Log in"]')
    }

    def login(self, *args) -> LoggedMainPage:
        self.login_field.set_text(args[0])
        self.password_field.set_text(args[1])
        self.signin_button.click_button()
        time.sleep(1)
        return LoggedMainPage(self.driver)


class MainPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "login_field": ('ID', 'login2')
    }

    def open_login(self) -> LoginPage:
        self.login_field.click_button()
        return LoginPage(self.driver)
