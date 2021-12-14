import requests
from datetime import datetime
from API_db_update import api_update_cities_db, api_update_restaurant_db
from config import RESTAURANTS_COLS, MAX_CHARS
import logging

NUM_OF_RESTS_PER_PAGE = 30
CURRENCY = "USD"
API_LOCATIONS_URL = "https://travel-advisor.p.rapidapi.com/locations/search"
API_RESTS_URL = "https://travel-advisor.p.rapidapi.com/restaurants/list"
API_REVIEWS_URL = "https://travel-advisor.p.rapidapi.com/restaurants/get-details"

HEADERS_LOCATION = {
    'x-rapidapi-host': "travel-advisor.p.rapidapi.com",
    'x-rapidapi-key': "22e2cc2258msh626c96a4012b38cp167d25jsn10e6c06452bf"
    }

MIN_REQ_STATUS_CODE = 200
MAX_REQ_STATUS_CODE = 400


class RestaurantFromAPI:
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
        award_list = []
        for award in self.rest_dict.get('awards'):
            award_dict = {k: award[k] for k in ['award_type', 'year']}
            award_list.append(award_dict)
        return award_list

    def get_reviews(self):
        review_query = {"location_id": self._rest_id, "currency": "USD", "lang": "en_US"}
        review_response = requests.request("GET", API_REVIEWS_URL, headers=HEADERS_LOCATION, params=review_query).json()
        response_reviews_list = review_response.get('reviews')
        reviews_list = []
        for review in response_reviews_list:
            review_dict = {'review_title': review['title'], 'rev_id': int(review['review_id']),
                           'review_text': review['summary'][:MAX_CHARS],
                           'date': datetime.strptime(review['published_date'].split('T')[0], '%Y-%m-%d'),
                           'user_name': review['author'], 'rate': int(review['rating'])}
            reviews_list.append(review_dict)
        return reviews_list

    def get_cuisines(self):
        cuisines = [cuis.get('name') for cuis in self.rest_dict.get('cuisine')]
        return cuisines


def get_city_data_API(city):
    querystring = {"query": city, "limit": '1', "currency": CURRENCY,
                   "sort": "relevance", "lang": "en_US"}
    response = requests.request("GET", API_LOCATIONS_URL, headers=HEADERS_LOCATION, params=querystring)

    # Checking response
    # if MIN_REQ_STATUS_CODE <= response.status_code < MAX_REQ_STATUS_CODE:
    #     logging.info('Cities requested successfully')
    # else:
    #     logging.error('Cities request failed')

    data = response.json()
    data = data['data'][0]['result_object']
    city_record = {'location_id': int(data['location_id']), 'city_name': data['name'],
                   'latitude': float(data['latitude']), 'longitude': float(data['longitude']),
                   'timezone': data['timezone'], 'num_reviews': int(data['num_reviews']),
                   'num_restaurants': int(data['category_counts']['restaurants']['total'])}
    return city_record


def get_rest_list_API(location_id, num_rests):
    querystring = dict(location_id=location_id, restaurant_tagcategory="10591",
                       restaurant_tagcategory_standalone="10591",
                       currency="USD", lunit="km", limit=num_rests, open_now="false", lang="en_US")
    response = requests.request("GET", API_RESTS_URL, headers=HEADERS_LOCATION, params=querystring)
    rests_data = response.json()['data']
    return rests_data


def scrape_cities_API(list_of_cities, num_rests):
    for city in list_of_cities:
        city_dict = get_city_data_API(city)
        api_update_cities_db(city_dict)
        location_id = city_dict['location_id']
        rests_list = get_rest_list_API(location_id, num_rests)
        for rest_dict in rests_list:
            if 'ad_position' not in rest_dict.keys():
                rest_obj = RestaurantFromAPI(rest_dict, location_id)
                api_update_restaurant_db(rest_obj)

# if __name__ == '__main__':
#     querystring = dict(location_id="293984", restaurant_tagcategory="10591", restaurant_tagcategory_standalone="10591",
#                        currency="USD", lunit="km", limit="30", open_now="false", lang="en_US")
#     response = requests.request("GET", API_RESTS_URL, headers=HEADERS_LOCATION, params=querystring)
#     data = response.json()['data']
#     for k in data:
#         print(k)
#     a = RestaurantFromAPI(data[4], 293984)
#     print('city record')
#     print(get_city_data_API('tel aviv'))
#     print('rest record')
#     print(a.get_rest_for_db())
#     print('cuisine record')
#     print(a.get_cuisines())
#     print('review record')
#     print(a.get_reviews())
#     print('award record')
#     print(a.get_awards())
