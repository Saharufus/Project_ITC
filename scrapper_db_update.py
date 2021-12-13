import re
from update_db import TableUpdate
import config
from datetime import datetime
from config import PRICING_RATE, CUISINE, CITY_RATE, REMOVE_HASH, NUM_TO_DIVIDE_RATING
from detailed_page_mining import *

# TODO: update in config
CUIS_FROM_TUPLE = 0

CITIES_COLS = ['location_id',
               'city_name',
               'num_restaurants',
               'timezone varchar',
               'num_reviews',
               'latitude',
               'longitude']

RESTAURANTS_COLS = ['res_id',
                    'location_id',
                    'res_name',
                    'rating',
                    'reviews_num',
                    'price_rate',
                    'city_rate',
                    'address',
                    'website varchar',
                    'phone varchar',
                    'latitude',
                    'longitude']

CUISINES_COLS = ['res_id',
                 'cuisine']

REVIEWS_COLS = ['rev_id',
                'user_name',
                'review_title',
                'res_id',
                'rate',
                'date',
                'review_text']

AWARDS_COLS = ['res_id',
               'award_type',
               'year']


def creating_restaurant_dict(rest):
    """
    Creating dictionary of restaurant data to insert db
    @param rest: Restaurants object from restaurant webpage
    @return: restaurant dictionary
    """
    # rest = RestaurantSoup(soup)
    name = rest.get_name()
    rest_dict = {}
    if name:
        cuisine, price_rate = rest.get_cuisine_and_price()
        details = [name,
                   rest.location_id,  # TODO: insert city id, correct db cols in config
                   rest.get_rating(),
                   rest.get_reviews_num(),
                   price_rate,
                   rest.get_city_rate(),
                   rest.get_address(),
                   rest.get_website(),
                   rest.get_phone()]
        rest_dict = dict(zip(config.RESTAURANTS_COLS, details))
    return rest_dict


def update_cities_table(city):
    """
    Updating cities table in MySQL DB
    @param city: dictionary with city  data
    @return: location_id (feature in cities table)
    """
    cities_table = TableUpdate(name='cities', data=city)
    location_id = city['location_id']
    return location_id


def update_restaurants_table(rest_dict):
    """
    Updating restaurants table in MySQL DB
    @param rest_dict: dictionary with restaurant data
    @return: res_id - the restaurant id in db (feature in table)
    """
    res_table = TableUpdate(name='restaurants',
                            data=rest_dict)
    res_table.insert_table()
    res_id = res_table.get_last_res_id()
    return res_id


def update_cuisines_table(cuis_list, res_id):
    """
    Updating cuisines table in MySQL DB
    @param cuis_list: list of cuisine types for a restaurant
    @param res_id: restaurant id from db
    """
    if cuis_list:
        for cuis in cuis_list:
            data = dict(zip(config.CUISINES_COLS, [res_id, cuis]))
            cuis_table = TableUpdate(name='cuisines',
                                     data=data)
            cuis_table.insert_table()


def update_reviews_table(reviews, res_id):
    """
    Updating cuisines table in MySQL DB
    @param reviews: list of reviews for a restaurant (list of dicts)
    @param res_id: restaurant id from db
    """
    for review in reviews:
        review.update({'res_id': res_id})
        rev_table = TableUpdate(name='reviews', data=review)
        rev_table.insert_table()


def update_awards_table(awards_list, res_id):
    """
    Updating cuisines table in MySQL DB
    @param awards_list: list of awards for a restaurant
    @param res_id: restaurant id from db
    """
    if awards_list:
        for award in awards_list:
            data = dict(zip(config.AWARDS_COLS, [res_id, award]))
            awards_table = TableUpdate(name='awards',
                                       data=data)
            awards_table.insert_table()


def scrapper_update_tables_in_db(soup, city_name):  # TODO: change the name detailed_page_mining (update_30_db) (previous name: update_tables_in_db)
    """
    Gets a soup object of a restaurant webpage from Tripadvisor and feed the db with mined data
    :param soup: soup object of restaurant webpage
    :param city_name: name of the city
    """
    rest = RestaurantSoup(soup)  # creating Restaurant object
    rest_dict = creating_restaurant_dict(rest)  # creating dictionary with restaurant details

    city_dict = {rest_dict['location_id']: city_name}  # creating dict to update cities table
    update_cities_table(city_dict)  # updating cities table

    res_id = update_restaurants_table(rest_dict)  # updating cities table + return res_id

    cuisines = rest.get_cuisine_and_price()[CUIS_FROM_TUPLE]  # getting cuisines list
    update_cuisines_table(cuisines, res_id)  # updating cuisines table

    reviews = rest.get_reviews()  # getting reviews list (list of dicts)
    update_reviews_table(reviews, res_id)  # updating reviews table

# def update_table_in_db(soup, city_name):
#     """
#     Gets a soup object of a restaurant webpage from Tripadvisor and feed the db with mined data
#     :param soup: soup object of restaurant webpage
#     :param city_name: name of the city
#     """
#     rest = RestaurantSoup(soup)
#     name = rest.get_name()
#     if name:
#         cuisine, price_rate = rest.get_cuisine_and_price()
#         details = [name,
#                    # rest.location_id,
#                    rest.get_rating(),
#                    rest.get_reviews_num(),
#                    price_rate,
#                    rest.get_city_rate(),
#                    rest.get_address(),
#                    rest.get_website(),
#                    rest.get_phone()]
#         rest_dict = dict(zip(config.RESTAURANTS_COLS, details))
#
#         res_table = TableUpdate(name='restaurants',
#                                 data=rest_dict)
#         res_table.insert_table()
#         res_id = res_table.get_last_res_id()
#         if cuisine:
#             for cuis in cuisine:
#                 data = dict(zip(config.CUISINES_COLS, [res_id, cuis]))
#                 cuis_table = TableUpdate(name='cuisines',
#                                          data=data)
#                 cuis_table.insert_table()
#
#         reviews = rest.get_reviews()
#         for review in reviews:
#             review.update({'res_id': res_id})
#             rev_table = TableUpdate(name='reviews', data=review)
#             rev_table.insert_table()
