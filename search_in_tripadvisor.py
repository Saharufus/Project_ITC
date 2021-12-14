from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import config
import logging

logging.basicConfig(filename='Tripadvisor scraper log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s', filemode='w')


def get_city_rest_url(city_name, driver):
    """
    Function returns city url in tripadvisor based on input city_name
    @param city_name: string - city name
    @param driver: A main driver to work on
    @return: string - url in for restaurants page of the city in tripadvisor
    """
    driver.get(config.WEBSITE_REST_URL)
    search = driver.find_elements(By.CSS_SELECTOR, "input.fhEMT._G.B-.z._J.Cj.R0")
    search[config.SEARCH_BOX].click()
    search[config.SEARCH_BOX].send_keys(city_name)
    time.sleep(2)
    html_from_page = driver.page_source
    soup = BeautifulSoup(html_from_page, 'html.parser')
    try:
        city_url = soup.find('a', class_="bPaPP w z _S _F Wc Wh Q B- _G", href=True)
        city_url = config.MAIN_PAGE + city_url['href']
        logging.info(f'Starting to scrape {city_name}\'s restaurants')
        return city_url
    except Exception:
        logging.warning(f'City named {city_name} not found')
