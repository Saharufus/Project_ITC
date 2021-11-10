from bs4 import BeautifulSoup
from selenium import webdriver
import config
from open_all_rest_in_page import get_list_of_soups
import pandas as pd
from next_page import next_page


def scrape_from_tripadvisor(city_name, file_name):
    """Scrapes Tripadvisor restaurants in a given city and saves the data to file_name.csv"""
    main_url = omers_function(city_name)  # a string of a url for the city page
    main_driver = webdriver.Chrome()

    list_of_dicts = []
    for i in range(config.START_PAGE, config.END_PAGE + 1):
        main_driver.get(main_url)
        main_soup = BeautifulSoup(main_driver.page_source, 'html.parser')

        list_of_restaurants_urls = bars_function_to_get_list_of_30_urls(main_soup)
        restaurant_soup_list = []
        get_list_of_soups(list_of_restaurants_urls, restaurant_soup_list)
        list_of_dicts.extend(bars_function_to_get_list_of_dicts(restaurant_soup_list))

        main_url = next_page(main_soup)

    main_driver.quit()
    data = pd.DataFrame(list_of_dicts)
    data.to_csv(file_name + '.csv')


