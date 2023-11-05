import pytest

from Homeworks.module_14.pages import MainPage, LoggedMainPage


def test_login(init_driver, user_test_data):
    main_page = MainPage(init_driver)
    login_page = main_page.open_login()

    try:
        login_page.login_field
    except Exception as e:
        pytest.fail(f"Username element wasn't found: {e}")

    try:
        login_page.password_field
    except Exception as e:
        pytest.fail(f"Password element wasn't found: {e}")

    logged_main_page = login_page.login(*user_test_data)

    try:
        assert logged_main_page.header.user_field.get_text() == f'Welcome {user_test_data[0]}'
    except Exception as e:
        pytest.fail(f"Username element wasn't found: {e}")

    try:
        assert logged_main_page.header.logout_field
    except Exception as e:
        pytest.fail(f"Log out element wasn't found: {e}")


def test_add_to_cart(logged_user, monitor_test_data):
    # open Monitors category
    logged_page = LoggedMainPage(logged_user)
    logged_page.open_monitors_list()

    # open the most expensive monitor
    sorted_monitors = logged_page.sort_products_desc()
    monitor_page = logged_page.open_product_page(sorted_monitors[0])

    # check product with expected name and price is opened
    assert monitor_page.name_field.get_text() == monitor_test_data[0]
    assert monitor_page.get_price() == monitor_test_data[1]

    # add Monitor to a cart
    monitor_page.add_product_to_cart()
    cart_page = logged_page.header.open_cart()
    products = cart_page.get_products()

    # check product with expected name and price is in the cart
    name_index = 1
    price_index = 2
    assert products[name_index].get_text() == monitor_test_data[0]
    assert products[price_index].get_text() == monitor_test_data[1]
