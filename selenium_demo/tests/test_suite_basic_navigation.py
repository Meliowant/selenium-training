from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import selenium_demo
import pytest
import os
import pathlib


@pytest.fixture
def browser(driver="geckodriver"):
    module_path = pathlib.Path(os.path.abspath(selenium_demo.__file__))
    geckodriver_path = module_path.parent / "drivers" / driver
    browser_ = webdriver.Firefox(executable_path=geckodriver_path)
    return browser_


@pytest.fixture
def main_page(browser, url="https://www.trust.com"):
    browser.get(url)
    yield browser
    browser.close()


def test_case_demo(browser):
    """
    Check if we can get geckodriver from python code
    """
    browser.get("https://www.trust.com/")
    #
    # This is legacy approach
    #
    # get_in_touch_button = browser.find_element_by_id("getInTouch-top")
    # message_area = browser.find_element_by_name("Message")
    # key_areas_container = browser.find_element_by_xpath(
    #     "//li[@class='pf-services']"
    # )
    # clients_list = browser.find_elements_by_class("swiper-slide")

    # Find top menu items
    menu_header = browser.find_element(By.CLASS_NAME, "menuHeader")
    assert menu_header
    menu_items = menu_header.find_elements(By.CLASS_NAME, "optionCont")
    assert len(menu_items) == 6

    # New approach
    # get_in_touch_button = browser.find_element(By.ID, "getInTouch-top")
    # message_area = browser.find_element(By.NAME, "Message")
    # services = browser.find_elements(By.XPATH, "//ul/[@class='pf-col pf-services--item']")
    # get_in_touch_button = browser.find_element(By.id, "getInTouch-top")
    assert True
    browser.close()


def test_case_main_menu_items(main_page):
    """
    Check all items in main menu
    """
    menu_items = [
        "PC & Laptop",
        "Mobile",
        "Smart Home",
        "Gaming",
        "Business",
        "Support",
    ]
    header = main_page.find_element(By.CLASS_NAME, "menuHeader")
    assert header
    items = header.find_elements(By.CLASS_NAME, "optionCont")
    assert len(items) == len(menu_items)
    for label in menu_items:
        element = header.find_element(
            By.XPATH,
            f'.//p[@class="txtCont"][text() = "{label}"]'
        )
        assert element, label
        assert element.is_displayed(), label
        assert element.is_enabled()

