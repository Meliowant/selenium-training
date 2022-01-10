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
        assert element.is_enabled(), label


def test_case_main_menu_items_have_menus_on_hover(main_page):
    """
    Check if main menu is detectable
    """
    menu_items = [
        "PC & Laptop",
        "Mobile",
        "Smart Home",
        "Gaming",
        "Business",
        "Support",
    ]
    for label in menu_items:
        menu_item = main_page.find_element(
            By.XPATH,
            ("//nav[@class='menuHeader']"
             f"//p[@class='txtCont'][text() = '{label}']")

        )
        assert menu_item
        submenu = menu_item.find_element(
            By.XPATH,
            (".//parent::a/following-sibling::div[@class='optionOverlayCont']")
        )
        assert submenu
    pass


@pytest.mark.skip
@pytest.mark.parametrize(
    "opts",
    [
        {
            "term": "",
            "dest_url": "",
        }
    ],
    ids=[]
)
def test_case_check_search(main_page, opts):
    """ Check if search works for the argument.
    """
    search_element = main_page.find_element(
        By.XPATH,
        "//nav[@class='menuSide']/button[@class='btnSearch search-open-button']"
    )
    search_field = main_page.find_element(
        By.XPATH,
        "/div[@class='search-input']"
    )

    assert search_element
    assert search_element.is_displayed(), "Search button is not visible"
    search_elememnt.click()
    assert search_field.is_displayed()
    search_element.send_keys("Aloha!")
    
