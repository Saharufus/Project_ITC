from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import pandas as pd

NUM_TO_DIVIDE_RATING = 10


def get_reviews_from_soup(soup):
    """
    @param soup: html text from tripadvisor website
    @return: dictionary with all reviews on html, keys: id, title, user_id, text( review content), rating, date
    """
    comments = soup.findAll('div', class_="reviewSelector")
    reviews_list = []
    for comment in comments:
        review_dict = {}
        review_dict['title'] = comment.find('span', class_='noQuotes').text
        review_dict['id'] = comment.get('data-reviewid')
        review_dict['text'] = comment.find('p', class_='partial_entry').text
        date = comment.find('span', class_='ratingDate').get('title')
        review_dict['date'] = datetime.strptime(date, '%B %d, %Y')
        review_dict['user_id'] = comment.find('div', class_="info_text pointer_cursor").text
        rating = comment.find('div', class_="ui_column is-9").find('span')
        review_dict['rating'] = int(int(rating['class'][1].split('_')[1]) / NUM_TO_DIVIDE_RATING)
        reviews_list.append(review_dict)
    return reviews_list

