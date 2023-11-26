from _pytest.fixtures import fixture
from selenium import webdriver

from Homeworks.module_14.pages import MainPage


@fixture(scope='function')
def logged_user(init_driver, user_test_data):
    driver = init_driver

    main_page = MainPage(driver)
    login_page = main_page.open_login()
    login_page.login(*user_test_data)
    yield driver


@fixture(scope='function')
def init_driver():
    driver = webdriver.Chrome()
    driver.get("https://www.demoblaze.com/")
    yield driver
    driver.close()


@fixture(scope='function')
def user_test_data():
    yield ("xomex52860@mainmile.com", "tmpxomex52860")


@fixture(scope='function')
def monitor_test_data():
    yield ("Apple monitor 24", "400")
