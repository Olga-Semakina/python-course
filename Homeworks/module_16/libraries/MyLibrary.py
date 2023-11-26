import operator

from selenium import webdriver
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from typing import List


class MyLibrary:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def sort_products_desc(self) -> List[WebElement]:
        selenium_lib = BuiltIn().get_library_instance('SeleniumLibrary')
        driver = selenium_lib.driver

        products_table = driver.find_element(By.ID, "tbodyid")
        products = products_table.find_elements(By.XPATH, ".//div[@class='card-block']")
        product_prices = dict()
        for product in products:
            price = product.find_element(By.XPATH, ".//*[contains(text(),'$')]").text.replace("$", "")
            product_prices.update({product: int(price)})
        products_sorted_desc = dict(sorted(product_prices.items(), key=operator.itemgetter(1), reverse=True))

        return list(products_sorted_desc.keys())

    def open_product_page(self, product_elem: WebElement):
        product_elem.find_element(By.XPATH, ".//a").click()
