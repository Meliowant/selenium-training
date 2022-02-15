from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_demo.tests.conftest import id_from_menuitem
from selenium.webdriver.common.keys import Keys
import selenium_demo
import pytest
import os
import pathlib


def id_from_name(arg):
    return arg.get("test_name").replace(" ", "_")


@pytest.fixture
def browser(driver="geckodriver"):
    module_path = pathlib.Path(os.path.abspath(selenium_demo.__file__))
    geckodriver_path = module_path.parent / "drivers" / driver
    ff_options = webdriver.firefox.options.Options()
    ff_options.add_argument("-headless")
    browser_ = webdriver.Firefox(
        executable_path=geckodriver_path, options=ff_options
    )
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


@pytest.mark.parametrize(
    "opts",
    [
        {
            "menu_item": "PC & Laptop",
            "sub_menus": [
                {
                    "title": "Keyboards & Mice",
                    "sections": [
                        "Mice",
                        "Mouse Pads",
                        "Keyboards",
                        "Keyboard and mouse combos"
                    ]
                },
                {
                    "title": "Home Office",
                    "sections": [
                        "Bundles",
                        "Keyboards & Mice",
                        "Webcams",
                        "Furniture"
                    ]
                },
                {
                    "title": "Sound & Vision",
                    "sections": [
                        "Speakers",
                        "Headsets",
                        "Microphones",
                        "Webcams"
                    ]
                },
                {
                    "title": "Videoconferencing",
                    "sections": [
                        "Overview",
                        "Iris Conference Camera",
                        "Accessories"
                    ]
                },
                {
                    "title": "Charging & Power",
                    "sections": [
                        "Chargers for laptops",
                        "Surge protection",
                        "UPS"
                    ]
                },
                {
                    "title": "Connect",
                    "sections": [
                        "Card readers",
                        "USB hubs",
                        "Converters & Adapters"
                    ]
                },
                {
                    "title": "Accessories",
                    "sections": [
                        "Laptop Bags & Sleeves",
                        "Laptop Stands",
                        "Presenters",
                        "Cooling fans"
                    ]
                }
            ]
        },
    ],
    ids=["PC & Laptop"]
)
def test_case_main_menu_items_have_menus(main_page, opts):
    """ Check if main menu has visible submenus """
    actions = ActionChains(main_page)
    menu_item = main_page.find_elements(
        By.XPATH,
        (
            "//nav[@class='menuHeader']//p[@class='txtCont']"
            f"[text() = '{opts['menu_item']}']/parent::a"
        )
    )
    assert menu_item
    assert len(menu_item) == 1  # There is only one such element

    menu_item = menu_item[0]
    assert menu_item.is_displayed()
    assert menu_item.is_enabled()

    submenu_container = menu_item.find_elements(
        By.XPATH,
        (
            "./following-sibling::div[@class='optionOverlayCont']"
        )
    )
    assert submenu_container
    assert len(submenu_container) == 1
    submenu_container = submenu_container[0]
    actions.move_to_element(menu_item)
    actions.perform()
    assert submenu_container.is_displayed()

    for submenu_params in opts["sub_menus"]:
        sm_title = submenu_container.find_elements(
            By.XPATH,
            (
                ".//*[@class='subOptionHeader closed']"
                f"[contains(text(), '{submenu_params['title']}')]"
            )
        )
        assert sm_title, submenu_params['title']
        assert len(sm_title) == 1
        sm_title = sm_title[0]
        assert sm_title.is_displayed()

        sm_section = sm_title.find_elements(
            By.XPATH,
            "./parent::div[@class='subOptionGrouping']"
        )
        assert sm_section
        assert len(sm_section) == 1
        sm_section = sm_section[0]
        assert sm_section.is_displayed()

        sub_items = sm_section.find_elements(
            By.XPATH,
            ".//div[@class='subOptionChildren']/a[@class='subOption']"
        )
        assert len(sub_items) == len(submenu_params["sections"])

        for sect in submenu_params["sections"]:
            sub_item = sm_section.find_elements(
                By.XPATH,
                (
                    "./div[@class='subOptionChildren']"
                    f"/a[@class='subOption'][text() = '{sect}']"
                )
            )
            assert sub_item, sect
            assert len(sub_item) == 1, sect
            sub_item = sub_item[0]
            assert sub_item.is_displayed()
            assert sub_item.is_enabled()


@pytest.mark.parametrize(
    "opts",
    [
        pytest.param(
            {
                "menu_item": "PC & Laptop",
                "submenus": [
                    "Keyboards & Mice",
                    "Home Office",
                    "Sound & Vision",
                    "Videoconferencing",
                    "Charging & Power",
                    "Connect",
                    "Accessories"
                ]
            },
            marks=pytest.mark.xfail(
                reason="Videoconferencing markup is broken"
            )
        ),
        {
            "menu_item": "Mobile",
            "submenus": ["Audio", "Power", "Travel", "Photo & Video"]
        },
        {
            "menu_item": "Smart Home",
            "submenus": ["WIFI", "Other"]
        },
        {
            "menu_item": "Gaming",
            "submenus": [
                "Control",
                "Gaming consoles",
                "Audio",
                "Furniture",
                "Accessories"
            ]
        },
        {
            "menu_item": "Business",
            "submenus": ["Solutions", "Video Conferencing", "Partners"]
        },
        pytest.param(
            {
                "menu_item": "Support",
                "submenus": ["Support", "Downloads", "Spareparts", "Contact"]
            },
            marks=pytest.mark.xfail(
                reason="Support markup is failed"
            )
        ),
    ],
    ids=id_from_menuitem
)
def test_case_main_menu_subitems_markup(main_page, opts):
    """Check proper markup in the submenu items"""
    for itm in opts["submenus"]:
        menu_item = main_page.find_elements(
            By.XPATH,
            (
                "//nav[@class='menuHeader']//p[@class='txtCont']"
                f"[text() = '{opts['menu_item']}']/parent::a"
                "/following-sibling::div[@class='optionOverlayCont']"
                f"//p[@class='subOptionHeader closed'][text() = '{itm}']"
            )
        )
        assert menu_item, f"Bad markup for '{opts['menu_item']}->{itm}'"
        assert len(menu_item) == 1


def test_case_check_search_is_present(main_page):
    """ Check if search button is present on the screen. """
    search_element = main_page.find_element(
        By.XPATH,
        "//nav[@class='menuSide']/button[@class='btnSearch search-open-button']"
    )
    assert search_element
    assert search_element.is_displayed(), "Search button is not visible"


def test_case_check_search_input_toggles(main_page):
    """ Check that search input expands and collapses as expected """
    search_button_switcher = main_page.find_element(
        By.XPATH,
        "//nav[@class='menuSide']"
        "/button[@class='btnSearch search-open-button']"
    )
    # Use CSS selector for search_box, as it appends new style class.
    # XPATH doesn't provide enough flexibility.
    search_field = main_page.find_element(
        By.CSS_SELECTOR, "div.search-box"
    )

    assert not search_field.is_displayed()
    search_button_switcher.click()
    assert not search_button_switcher.is_displayed()
    assert search_field.is_displayed()

    search_bar_btns_css = [
        "svg.magnifying-glass",
        "form.search-form",
        "div.search-close-button",
        "a.i-button"
    ]
    for btn_css in search_bar_btns_css:
        element = search_field.find_element(By.CSS_SELECTOR, btn_css)
        assert element.is_displayed()

    search_field.find_element(
        By.CSS_SELECTOR, "div.search-close-button"
    ).click()
    WebDriverWait(main_page, 10).until_not(EC.visibility_of(search_field))
    assert not search_field.is_displayed()

    for btn_css in search_bar_btns_css:
        element = search_field.find_element(By.CSS_SELECTOR, btn_css)
        assert not element.is_displayed()

    assert search_button_switcher.is_displayed()


@pytest.mark.parametrize(
    "opts",
    [
        {
            "test_name": "Empty query",
            "query": "",
            "expected_help_text": (
                "Our support is organized by product. First you will need to "
                "find your product, then you will be able to get support, "
                "information, downloads, etc."
            ),
            "has_items": False,
        },
        {
            "test_name": "Non-empty query",
            "query": "test",
            "expected_help_text": "",
            "has_items": True,
        },
    ],
    ids=id_from_name
)
def test_case_check_search_redirects(main_page, opts):
    """ Check if search button works correctly """
    search_button_toggler = main_page.find_element(
        By.CLASS_NAME, "search-open-button"
    )
    search_field = main_page.find_element(
        By.CSS_SELECTOR, "form.search-form > input.search-input"
    )
    search_button_toggler.click()
    assert search_field
    search_field.send_keys(opts["query"], Keys.RETURN)

    WebDriverWait(main_page, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.c-search-results")
        )
    )
    search_results = main_page.find_element(
        By.CSS_SELECTOR, "div.c-search-results > section"
    )
    assert search_results
    assert search_results.text == "Searching for something?"

    search_help = search_results.find_element(
        By.XPATH,
        "//parent::section/following-sibling::div[@class='l-grid']//p"
    )
    assert search_help
    assert opts["expected_help_text"] in search_help.text

    search_items = search_results.find_elements(
        By.XPATH,
        "//parent::section/following-sibling::div[@class='l-grid']"
        "//div[@class='c-card has--radius']"
    )
    assert (len(search_items) > 0) is opts["has_items"]


def test_case_check_banner(main_page):
    """ Check if we have a correct banner on the first page """
    banner = main_page.find_element(By.CLASS_NAME, "c-key-visual-header")
    assert banner.is_displayed()
    banner_url = banner.find_element(By.XPATH, ".//parent::a")
    assert banner_url.get_dom_attribute("href") == "/en/campaigns/webcams"
    banner_text = banner.find_element(By.CLASS_NAME, "c-key-visual-header__text")
    assert banner_text.text == "First impressions\nare only made once"
    banner_highlighted_text = banner_text.find_element(
        By.XPATH, "./h1/span"
    )
    assert banner_highlighted_text.value_of_css_property(
        "color"
    ) == "rgb(224, 32, 27)"
    banner_regular_text = banner_text.find_element(
        By.XPATH, ".//parent::h1"
    )
    assert banner_regular_text.value_of_css_property(
        "color"
    ) == "rgb(14, 12, 56)"


def test_case_check_banner_button(main_page):
    """ Check button "Discover more" at the banner """
    banner_button = main_page.find_element(
        By.XPATH,
        "//div[contains(@class, 'btn')][contains(text(), 'Discover more')]"
    )
    assert banner_button
    assert banner_button.value_of_css_property(
        "background-color"
    ) == "rgb(255, 228, 0)"
    banner_button.click()
    WebDriverWait(main_page, 10).until(
        EC.url_changes("https://www.trust.com/en/")
    )
    assert main_page.current_url == \
        "https://www.trust.com/en/campaigns/webcams"


def test_case_check_featured_products_presence(main_page):
    """ Check if section 'Featured products' is present on the main page """
    fp_section_header = main_page.find_element(
        By.XPATH,
        (
            "//div[@class='l-maxwidth']/"
            "h2[contains(@class, 'h2')][contains(text(), 'Featured products')]"
        )
    )
    assert fp_section_header.is_displayed()

    fp_section = fp_section_header.find_element(
        By.XPATH, ".//parent::div[@class='l-maxwidth']"
    )
    assert fp_section

    products_container = fp_section.find_element(
        By.CSS_SELECTOR, "div.swiper-container-product-card"
    )
    assert products_container

    scroll_left_button = products_container.find_element(
        By.CLASS_NAME, "swiper-button-prev"
    )
    scroll_right_button = fp_section.find_element(
        By.CSS_SELECTOR, "div.swiper-button-next"
    )
    featured_products_list = fp_section.find_element(
        By.XPATH, ".//div[@class='swiper-wrapper']"
    )


@pytest.mark.xfail(reason="visibility attribute is set to hidden")
@pytest.mark.parametrize(
    "btn", ["prev", "next"], ids=["previous button", "next button"]
)
def test_case_check_featured_products_scroll_buttons_visible(main_page, btn):
    """ Check if scrolling with button is working as expected """
    fp_scroll_btn = main_page.find_element(
        By.CSS_SELECTOR, f"div.swiper-button-{btn}"
    )
    assert fp_scroll_btn.is_displayed()
