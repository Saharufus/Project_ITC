import requests
from datetime import datetime
from API_db_update import api_update_restaurant_db
import logging
from detailed_page_mining import update_cities_table
import pymysql
from config import *


class RestaurantFromAPI:
    """
    Class used to get relevant data for db update using Travel Advisor API - rests, cuisines, reviews, awards
    """

    def __init__(self, rest_dict, location_id):
        self.rest_dict = rest_dict
        self._rest_id = rest_dict.get('location_id')
        self.res_name = rest_dict.get('name')
        self.rating = rest_dict.get('rating')
        if self.rating:
            self.rating = float(self.rating)
        self.reviews_num = rest_dict.get('num_reviews')
        if self.reviews_num:
            self.reviews_num = int(self.reviews_num)
        self.price_rate = rest_dict.get('price_level')
        self.city_rate = rest_dict.get('ranking_position')
        if self.city_rate:
            self.city_rate = int(self.city_rate)
        self.address = rest_dict.get('address')
        self.website = rest_dict.get('website')
        self.phone = rest_dict.get('phone')
        self.latitude = rest_dict.get('latitude')
        if self.latitude:
            self.latitude = float(self.latitude)
        self.longitude = rest_dict.get('longitude')
        if self.longitude:
            self.longitude = float(self.longitude)
        self.location_id = location_id

    def get_rest_for_db(self):
        """
        @return: dictionary of rest data in db required format
        """
        details = [self.res_name,
                   self.location_id,
                   self.rating,
                   self.reviews_num,
                   self.price_rate,
                   self.city_rate,
                   self.address,
                   self.website,
                   self.phone,
                   self.latitude,
                   self.longitude,
                   self.location_id]
        return dict(zip(RESTAURANTS_COLS, details))

    def get_awards(self):
        """
        @return: dictionary of Tripadvisor awards data in db required format per restaurant
        """
        award_list = []
        for award in self.rest_dict.get('awards'):
            award_dict = {k: award[k] for k in ['award_type', 'year']}
            award_list.append(award_dict)
        return award_list

    def get_reviews(self):
        """
        @return: list of reviews dictionary in db required format per restaurant
        """
        review_query = {"location_id": self._rest_id, "currency": CURRENCY, "lang": LANG}
        review_response = requests.request("GET", API_REVIEWS_URL, headers=HEADERS_LOCATION, params=review_query)
        if MIN_REQ_STATUS_CODE <= review_response.status_code < MAX_REQ_STATUS_CODE:
            logging.info(f'Reviews requested successfully for rest {self.res_name}')
        else:
            err = 'Reviews request failed'
            logging.error(err)
            raise ConnectionError(err)
        review_response = review_response.json()
        response_reviews_list = review_response.get('reviews')
        reviews_list = []
        if response_reviews_list:
            for review in response_reviews_list:
                review_dict = {'review_title': review['title'], 'rev_id': int(review['review_id']),
                               'review_text': review['summary'][:MAX_CHARS],
                               'date': datetime.strptime(review['published_date'].split('T')[0], '%Y-%m-%d'),
                               'user_name': review['author'], 'rate': int(review['rating'])}
                reviews_list.append(review_dict)
        return reviews_list

    def get_cuisines(self):
        """
        @return:  list of cuisines per restaurant

        """
        cuisines = [cuis.get('name') for cuis in self.rest_dict.get('cuisine')]
        return cuisines


def get_city_data_API(city):
    """
    Retrieves city information from API
    @param city: city name
    @return: city_record - dictionary of city data
    """
    querystring = {"query": city, "limit": '1', "currency": CURRENCY,
                   "sort": SORT_METHOD, "lang": LANG}
    response = requests.request("GET", API_LOCATIONS_URL, headers=HEADERS_LOCATION, params=querystring)
    if MIN_REQ_STATUS_CODE <= response.status_code < MAX_REQ_STATUS_CODE:
        logging.info('Cities requested successfully')
    else:
        err = 'Cities request failed'
        logging.error(err)
        raise ConnectionError(err)

    data = response.json()
    try:
        data = data['data'][0]['result_object']
        city_record = {'location_id': int(data['location_id']), 'city_name': data['name'],
                       'latitude': float(data['latitude']), 'longitude': float(data['longitude']),
                       'timezone': data['timezone'], 'num_reviews': int(data['num_reviews']),
                       'num_restaurants': int(data['category_counts']['restaurants']['total'])}
        return city_record
    except IndexError:
        err = f'City {city} request failed'
        logging.error(err)
        raise IOError(err)


def get_rest_list_API(location_id, num_pages):
    """
    @param location_id: unique tripadvisor identifier per city
    @param num_pages: amount of pages to scan
    @return: list of restaurant records
    """
    rests_data = []
    for i in range(num_pages):
        querystring = dict(location_id=location_id, restaurant_tagcategory=RESTAURANT_TAGCATEGORY,
                           restaurant_tagcategory_standalone=RESTAURANT_TAGCATEGORY,
                           currency=CURRENCY, lunit=LUNIT, limit=NUM_OF_RESTS_PER_PAGE, open_now="false", lang=LANG,
                           offset=i * NUM_OF_RESTS_PER_PAGE)
        response = requests.request("GET", API_RESTS_URL, headers=HEADERS_LOCATION, params=querystring)
        if MIN_REQ_STATUS_CODE <= response.status_code < MAX_REQ_STATUS_CODE:
            logging.info('Restaurants requested successfully')
        else:
            err = 'Restaurants request failed'
            logging.error(err)
            raise ConnectionError(err)
        rests_data = rests_data + response.json()['data']
    return rests_data


def scrape_cities_API(list_of_cities, num_rests):
    """
    Creates restaurant object and update db
    @param list_of_cities: list of cities to scrape from API
    @param num_rests: amount of requested restaurants to retrieve
    """
    for city in list_of_cities:
        try:
            city_dict = get_city_data_API(city)
            update_cities_table(city_dict)
            location_id = city_dict['location_id']
            rests_list = get_rest_list_API(location_id, num_rests)
            for rest_dict in rests_list:
                if 'ad_position' not in rest_dict.keys():
                    rest_obj = RestaurantFromAPI(rest_dict, location_id)
                    api_update_restaurant_db(rest_obj)
        except ConnectionError:
            print(
                'One of your API connections  failed - please check your keys and URLs - For more info check the logs')
        except IOError as err:
            print(err)
        except pymysql.err.OperationalError:
            err = 'Connection to MySQL server failed, please check your credentials'
            print(err)
            logging.error(err)
