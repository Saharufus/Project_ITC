from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException


def open_n_rest_tabs(url_short_list, driver, empty_list):
    """
    Fills a list with soups of restaurants from sublist of urls
    :param url_short_list: A sub list of the list of restaurants urls in one page
    :param driver: A main driver to work on
    :param empty_list: List to be filled with soups
    """
    for url in url_short_list:
        driver.execute_script(f"window.open('{url}');")

    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        try:
            empty_list.append(BeautifulSoup(driver.page_source, 'html.parser'))
            driver.close()
        except WebDriverException:
            pass


def get_list_of_soups_main_page_url_tabs(url_list, driver, empty_list, threads):
    """
    Fills a list with soups of restaurants from list of urls
    :param url_list: List of urls of 30 restaurants in main page
    :param driver: A main driver to work on
    :param empty_list: List to be filled with soups
    :param threads: Number of tabs to open simultaneously
    """
    for i in range(int(len(url_list) / threads)):
        open_n_rest_tabs(url_list[i*threads:(i+1)*threads], driver, empty_list)
        driver.switch_to.window(driver.window_handles[0])

