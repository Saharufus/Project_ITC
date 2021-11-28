from search_in_tripadvisor import get_city_rest_url
from get_rest_url_list import get_rest_url_list
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from next_page import next_page
from bs4 import BeautifulSoup
import config


# setup
def setup_driver():
    options = Options()
    options.headless = True
    driver = Chrome(options=options)
    return driver


def test_get_city_url_success():
    # setup
    driver = setup_driver()

    # test
    url_1 = get_city_rest_url('tel aviv', driver)
    url_2 = get_city_rest_url('new york', driver)
    assert url_1 == "https://www.tripadvisor.com//Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html"
    assert url_2 == "https://www.tripadvisor.com//Restaurants-g60763-New_York_City_New_York.html"


def test_next_page_success():
    # setup
    driver = setup_driver()
    driver.get(get_city_rest_url('tel aviv', driver))

    # testing 5 next pages
    for i in range(1, 6):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        url = next_page(soup)
        assert url == f"https://www.tripadvisor.com//Restaurants-g293984-oa{i*30}-Tel_Aviv_Tel_Aviv_District.html#EATERY_LIST_CONTENTS"
        driver.get(url)


def test_get_rest_url_list_success():
    # setup
    with open("test_html.html", 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')
    list_to_test = get_rest_url_list(soup)
    assert len(list_to_test) == 2
    assert list_to_test[0] == config.MAIN_PAGE + 'Great!!!'
    assert list_to_test[1] == config.MAIN_PAGE + 'Amazing'
