from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from time import sleep

REVIEWS = 0
SIZE_OF_REVIEW = 3
TYPE_OF_REST = 0
PRICE = 1
PAGE_START = 'https://www.tripadvisor.com/Restaurants-g'
CITY_DICT = {'Tel-Aviv': 293984}


def what_is_in(type_or_price):
    """Gets the type and price of a restaurant"""
    if len(type_or_price) == 2:
        type_of_rest = type_or_price[TYPE_OF_REST].text
        price_of_rest = type_or_price[PRICE].text
    elif len(type_or_price) == 1:
        if '$' in type_or_price[TYPE_OF_REST].text:
            type_of_rest = None
            price_of_rest = type_or_price[TYPE_OF_REST].text
        else:
            type_of_rest = type_or_price[TYPE_OF_REST].text
            price_of_rest = None
    else:
        type_of_rest = None
        price_of_rest = None
    return type_of_rest, price_of_rest


def choose_city_and_page(city_name, page_number):
    """Returns the url of Tripadvisor restaurants with the city and page chosen"""
    return PAGE_START + str(CITY_DICT[city_name]) + f'-oa{30*(page_number-1)}'


def food_scraper(file_name, city, first_page=1, last_page=2):
    """
    Scrapes data from Tripadvisor. Creates *.csv file that contains:
        1. Name of restaurant
        2. Average review (0 - 5)
        3. Number of reviews
        4. Type of food
        5. Expense
    :file_name: The name of the csv ==> file_name.csv
    :city: Name of the city you want to scrape from (in capitals)
    :first_page: The page to start the scrape in the site
    :last_page: The page to finish the scrape
    """
    driver = webdriver.Chrome()
    list_of_rest = []
    for page_num in range(first_page, last_page+1):
        # getting website html code
        driver.get(choose_city_and_page(city, page_num))
        sleep(1)
        html_text = BeautifulSoup(driver.page_source, 'html.parser')

        # getting the wanted card with info of the restaurants
        content = html_text.find_all('div', class_='emrzT Vt o')

        for restaurant in content:
            rest_name = restaurant.find('a', class_='bHGqj Cj b').text
            if rest_name[0].isdigit():  # get rid of the sponsored
                avg_review_text = restaurant.find('svg', class_='RWYkj d H0')
                avg_review = float(avg_review_text.get('title')[:SIZE_OF_REVIEW])
                num_of_reviews = restaurant.find('span', class_='NoCoR').text.split()[REVIEWS]
                reviews_type_price = restaurant.find('div', class_='bhDlF bPJHV eQXRG').find_all('span', class_='XNMDG')
                food_type, price = what_is_in(reviews_type_price)

                table = {'Restaurant name': rest_name.lstrip('0123456789. '),
                         'Review': avg_review,
                         'Number of reviews': num_of_reviews,
                         'Restaurant type': food_type,
                         'Price': price
                         }

                list_of_rest.append(table)

    driver.quit()
    data = pd.DataFrame(list_of_rest)
    data.to_csv(file_name + '.csv')


# def main():




food_scraper('rest_TLV', 'Tel-Aviv', 1, 5)
