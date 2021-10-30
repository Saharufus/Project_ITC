from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

NUMBER_OF_REVIEWS = 0
REVIEWS = 0
SIZE_OF_REVIEW = 3
FIRST_RESTAURANT = 1
TYPE_OF_REST = 0
PRICE = 1

driver = webdriver.Chrome()
driver.get('https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html')
html_text = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

content = html_text.find_all('div', class_='emrzT Vt o')
list_of_rest = []
for restaurant in content[FIRST_RESTAURANT:]:
    rest_name = restaurant.find('a', class_='bHGqj Cj b').text.lstrip('0123456789. ')
    avg_review_text = restaurant.find('svg', class_='RWYkj d H0')
    avg_review = float(avg_review_text.get('title')[:SIZE_OF_REVIEW])
    num_of_reviews = restaurant.find('span', class_='NoCoR').text.split()[REVIEWS]
    reviews_type_price = restaurant.find('div', class_='bhDlF bPJHV eQXRG').find_all('span', class_='XNMDG')
    food_type = reviews_type_price[TYPE_OF_REST].text
    price = reviews_type_price[PRICE].text

    table = {'Restaurant name': rest_name,
             'Review': avg_review,
             'Number of reviews': num_of_reviews,
             'Restaurant type': food_type,
             'Price': price
             }

    list_of_rest.append(table)

data = pd.DataFrame(list_of_rest)
print(data)
data.to_csv('Restaurants.csv')
