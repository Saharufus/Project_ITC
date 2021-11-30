from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from config import NEW_TAB, MAIN_TAB


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
        driver.switch_to.window(driver.window_handles[NEW_TAB])
        try:
            empty_list.append(BeautifulSoup(driver.page_source, 'html.parser'))
            driver.close()
        except WebDriverException:
            pass


def get_list_of_soups_main_page_url_tabs(url_list, driver, threads):
    """
    Fills a list with soups of restaurants from list of urls
    :param url_list: List of urls of 30 restaurants in main page
    :param driver: A main driver to work on
    :param threads: Number of tabs to open simultaneously
    """
    soup_list = []
    for i in tqdm(range(len(url_list) // threads)):
        open_n_rest_tabs(url_list[i*threads:(i+1)*threads], driver, soup_list)
        driver.switch_to.window(driver.window_handles[MAIN_TAB])
    return soup_list
