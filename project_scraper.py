from bs4 import BeautifulSoup
from selenium import webdriver
import re

NUMBER_OF_REVIEWS = 0
REVIEW = 0

driver = webdriver.Chrome()
driver.get('https://www.tripadvisor.com/Restaurants-g293984-Tel_Aviv_Tel_Aviv_District.html')
html_text = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

rest_names_html = html_text.find_all('a', class_='bHGqj Cj b')
num_of_reviews_html = html_text.find_all('a', class_='dMdkg _S')
avg_review_html = html_text.find_all('svg', class_='RWYkj d H0', viewbox="0 0 88 16")

rest_names = [x.text.lstrip('0123456789. ') for x in rest_names_html]
num_of_reviews = [int(re.findall('[0-9]+', x.text)[NUMBER_OF_REVIEWS]) for x in num_of_reviews_html]
avg_review = [float(x.get('title').split()[REVIEW]) for x in avg_review_html]

for i, rest in enumerate(rest_names):
    print((rest, num_of_reviews[i], avg_review[i]))
