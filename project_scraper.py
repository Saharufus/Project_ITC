from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from time import sleep

REVIEWS = 0
SIZE_OF_REVIEW = 3
FIRST_RESTAURANT = 1
TYPE_OF_REST = 0
PRICE = 1
FIRST_PAGE = 'https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html'
PAGE_TO_START = 1
PAGE_TO_END = 5


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


def choose_page(page_number):
    """Returns next page url"""
    return FIRST_PAGE[:48] + f'oa{30*(page_number-1)}-' + FIRST_PAGE[48:]


driver = webdriver.Chrome()
list_of_rest = []
for page_num in range(PAGE_TO_START, PAGE_TO_END):
    # getting website html code
    driver.get(choose_page(page_num))
    sleep(3)
    html_text = BeautifulSoup(driver.page_source, 'html.parser')

    # getting the wanted card with info of the restaurants
    content = html_text.find_all('div', class_='emrzT Vt o')

    for restaurant in content[FIRST_RESTAURANT:]:
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
print(data)
data.to_csv('Restaurants.csv')
