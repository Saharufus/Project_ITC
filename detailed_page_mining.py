import re
import pymysql.err
import logging
from update_db import TableUpdate
from datetime import datetime
from config import *


# Data mining of each restaurant: using RestaurantSoup object:
class RestaurantSoup:
    def __init__(self, soup):
        self.soup = soup

    def get_name(self):
        try:
            name = (self.soup.find('div', class_="eTnlN _W w O")).find('h1', class_="fHibz").text
        except AttributeError:
            name = None
        return name

    def get_rating(self):
        try:
            rating = float(self.soup.find('span', class_="fdsdx").text.strip('"'))
        except AttributeError:
            rating = None
        return rating

    def get_reviews_num(self):
        try:
            reviews_num = int(re.sub("[^0-9]", "", self.soup.find('a', class_="dUfZJ").text))
        except AttributeError:
            reviews_num = None
        return reviews_num

    def get_cuisine_and_price(self):
        try:
            details = self.soup.find('span', class_="dyeJW VRlVV").find_all('a', class_="drUyy")
            details_list = [det.text for det in details]
            if len(details_list) == 0:
                price_rate = None
                cuisine = None
            elif '$' in details_list[PRICING_RATE]:
                price_rate = details_list[PRICING_RATE]
                if len(details_list) > 1:
                    cuisine = details_list[CUISINE:]
                else:
                    cuisine = None
            else:
                price_rate = None
                cuisine = details_list
        except AttributeError:
            price_rate = None
            cuisine = None
        return cuisine, price_rate

    def get_city_rate(self):
        try:
            city_rate = self.soup.find('div', class_="fYCpi").text.split()[CITY_RATE][REMOVE_HASH:]
        except AttributeError:
            city_rate = None
        return city_rate

    def get_address(self):
        try:
            address = self.soup.find('span', class_="brMTW").text
        except AttributeError:
            address = None
        return address

    def get_website(self):
        try:
            website = self.soup.find('div', class_="bKBJS Me enBrh").find('a').get("href")
        except AttributeError:
            website = None
        return website

    def get_phone(self):
        try:
            phone = self.soup.find('div', class_="bKBJS Me").find('a').get("href").strip('tel:')
        except AttributeError:
            phone = None
        return phone

    def get_reviews(self):
        """
        @return: dictionary with all reviews on html, keys: id, title, user_id, text( review content), rating, date
        """
        comments = self.soup.findAll('div', class_="reviewSelector")
        reviews_list = []
        for comment in comments:
            date = comment.find('span', class_='ratingDate').get('title')
            rating = comment.find('div', class_="ui_column is-9").find('span')
            review_dict = {'review_title': comment.find('span', class_='noQuotes').text,
                           'rev_id': comment.get('data-reviewid'),
                           'review_text': comment.find('p', class_='partial_entry').text[:MAX_CHARS],
                           'date': datetime.strptime(date, '%B %d, %Y'),
                           'user_name': comment.find('div', class_="info_text pointer_cursor").text,
                           'rate': int(int(rating['class'][1].split('_')[1]) / NUM_TO_DIVIDE_RATING)}
            reviews_list.append(review_dict)
        return reviews_list


# Updating data of each restaurant in database:
def update_30_db(soups, city_name, city_id):
    """
    The function accepts a list of soups (html text) of detailed restaurant pages
    and updates table with soups batch
    @param soups: list of BeautifulSoup objects (html text)
    @param city_name: name of the scraped city
    @param city_id: location id of city
    """
    for soup in soups:
        try:
            update_tables_in_db(soup, city_name, city_id)
        except pymysql.err.OperationalError:
            err = 'Connection to MySQL server failed, please check your credentials'
            raise ConnectionError(err)


def creating_restaurant_dict(rest, city_id):
    """
    Creating dictionary of restaurant data to insert db
    @param rest: Restaurants object from restaurant webpage
    @param city_id: city id from db
    @return: restaurant dictionary
    """
    name = rest.get_name()
    rest_dict = {}
    if name:
        cuisine, price_rate = rest.get_cuisine_and_price()
        details = [name,
                   city_id,
                   rest.get_rating(),
                   rest.get_reviews_num(),
                   price_rate,
                   rest.get_city_rate(),
                   rest.get_address(),
                   rest.get_website(),
                   rest.get_phone()]
        rest_dict = dict(zip(RESTAURANTS_COLS, details))
    return rest_dict


def update_cities_table(city):
    """
    Updating cities table in MySQL DB
    @param city: dictionary with city  data
    """

    cities_table = TableUpdate(name=CITIES_TAB, data=city)
    cities_table.insert_table()
    logging.info(f'table: {CITIES_TAB} updated with city: {city["city_name"]}')


def update_restaurants_table(rest_dict):
    """
    Updating restaurants table in MySQL DB
    @param rest_dict: dictionary with restaurant data
    @return: res_id - the restaurant id in db (feature in table)
    """
    res_table = TableUpdate(name=RES_TAB, data=rest_dict)
    res_table.insert_table()
    res_id = res_table.get_last_res_id()
    if res_id:
        logging.info(f'table {RES_TAB} updated with rest: {rest_dict["res_name"]}')
    else:
        logging.info(f'rest {rest_dict["res_name"]} already exists in db')
    return res_id


def update_cuisines_table(cuis_list, res_id):
    """
    Updating cuisines table in MySQL DB
    @param cuis_list: list of cuisine types for a restaurant
    @param res_id: restaurant id from db
    """
    if cuis_list:
        for cuis in cuis_list:
            data = dict(zip(CUISINES_COLS, [res_id, cuis]))
            cuis_table = TableUpdate(name=CUIS_TAB, data=data)
            cuis_table.insert_table()
        if res_id:
            logging.info(f'table: {CUIS_TAB} updated for rest {res_id}')


def update_reviews_table(reviews, res_id):
    """
    Updating cuisines table in MySQL DB
    @param reviews: list of reviews for a restaurant (list of dicts)
    @param res_id: restaurant id from db
    """
    if reviews:
        for review in reviews:
            review.update({'res_id': res_id})
            rev_table = TableUpdate(name=REV_TAB, data=review)
            rev_table.insert_table()
        if res_id:
            logging.info(f'table: {REV_TAB} updated for rest {res_id}')


def update_awards_table(awards, res_id):
    """
    Updating cuisines table in MySQL DB
    @param awards: list of awards dictionaries for a restaurant
    @param res_id: restaurant id from db
    """
    if awards:
        for award in awards:
            award.update({'res_id': res_id})
            awards_table = TableUpdate(name=AWARDS_TAB, data=award)
            awards_table.insert_table()
        if res_id:
            logging.info(f'table: {AWARDS_TAB} updated for rest {res_id}')


def update_tables_in_db(soup, city_name, city_id):
    """
    Gets a soup object of a restaurant webpage from Tripadvisor and feed the db with mined data
    @param: soup: soup object of restaurant webpage
    @param: city_name: name of the city
    @param: city_id: location_id of city
    """
    rest = RestaurantSoup(soup)  # creating Restaurant object
    rest_dict = creating_restaurant_dict(rest, city_id)  # creating dictionary with restaurant details

    city_dict = dict(zip(CITIES_COLS[:CITIES_FOR_SCRAPER],
                         [city_id, city_name]))  # creating city dict
    update_cities_table(city_dict)  # updating cities table

    res_id = update_restaurants_table(rest_dict)  # updating cities table + return res_id

    cuisines = rest.get_cuisine_and_price()[CUIS_FROM_TUPLE]  # getting cuisines list
    update_cuisines_table(cuisines, res_id)  # updating cuisines table

    reviews = rest.get_reviews()  # getting reviews list (list of dicts)
    update_reviews_table(reviews, res_id)  # updating reviews table
