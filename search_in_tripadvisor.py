from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

WEBSITE_PARENT_URL = "https://www.tripadvisor.com"
WEBSITE_REST_URL = "https://www.tripadvisor.com/Restaurants"

def get_city_rest_url(city_name):
    """
    Function returns city url in tripadvisor based on inpur city_name
    :param city_name: string - city name
    :return: string - url in for restaurants page of the city in tripadvisor
    """

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(WEBSITE_REST_URL)
    search = driver.find_elements(By.CSS_SELECTOR, "input.fhEMT._G.B-.z._J.Cj.R0")
    search[1].click()
    search[1].send_keys(city_name)
    time.sleep(2)
    html_from_page = driver.page_source
    soup = BeautifulSoup(html_from_page, 'html.parser')
    city_url = soup.find('a', class_="bPaPP w z _S _F Wc Wh Q B- _G", href= True)
    city_url = WEBSITE_PARENT_URL + city_url['href']
    return city_url

if __name__ == '__main__':
    print(get_city_rest_url('amsterdam'))
