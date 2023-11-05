from seleniumpagefactory.Pagefactory import PageFactory
from selenium import webdriver


class LoginPage(PageFactory):
    def __init__(self, driver):
        self.driver = driver

    locators = {
        "login_field": ('ID', 'user-name'),
        "password_field": ('XPATH', '//*[@type="password"]'),
        "signin_button": ('CSS', 'input[class="submit-button btn_action"]')
    }

    def login(self, *user_info) -> str:
        self.login_field.set_text(user_info[0])
        self.password_field.set_text(user_info[1])
        self.signin_button.click_button()
        return self.driver.current_url


def test_login():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    login_page = LoginPage(driver)
    user_info = ("visual_user", "secret_sauce")
    current_url = login_page.login(*user_info)
    expected_url = "https://www.saucedemo.com/inventory.html"
    assert current_url == expected_url

    driver.close()
