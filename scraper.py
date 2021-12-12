from search_in_tripadvisor import get_city_rest_url
from get_rest_url_list import get_rest_url_list
from next_page import next_page
from open_rest_in_tabs import get_list_of_soups_main_page_url_tabs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from detailed_page_mining import update_30_db
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scrape_from_tripadvisor(city_name, pages, main_driver, threads=5):
    """
    Performs scrape and updating db per city user input
    @param city_name: name of the city to scrape restaurants from
    @param pages: number of rests pages to scrape
    @param main_driver: browser driver object
    @param threads: number of threads
    """
    main_url = get_city_rest_url(city_name, main_driver)
    for page in range(pages):
        main_driver.get(main_url)
        main_soup = BeautifulSoup(main_driver.page_source, 'html.parser')
        list_of_restaurants_urls = get_rest_url_list(main_soup)
        restaurant_soup_list = get_list_of_soups_main_page_url_tabs(list_of_restaurants_urls, main_driver, threads)
        update_30_db(restaurant_soup_list, city_name)
        main_url = next_page(main_soup)


def scrape_list_of_cities(list_of_cities, pages, threads=5):
    """
    Main Function - fills db for all cities using helper functions
    @param list_of_cities: list of cities received from user input
    @param pages: number of pages to scrape per city
    @param threads: number of threads
    """
    options = Options()
    options.headless = True
    s = Service(ChromeDriverManager().install())
    main_driver = webdriver.Chrome(service=s)
    for city in list_of_cities:
        scrape_from_tripadvisor(city, pages, main_driver, threads)
    main_driver.quit()
