from scrapper_db_update import update_cities_table, update_restaurants_table, \
    update_cuisines_table, update_reviews_table, update_awards_table
from API_scraper import *

#TODO: insert to main with api mining, with "scrape_city_API"
#TODO: loop on cities list?? maybe add to scrape_cities_API(list_of_cities, num_rests) in API_SCRAPER

def api_update_tables_in_db(city_name):
    """
    Gets a soup object of a restaurant webpage from Tripadvisor and feed the db with mined data
    :param city_name: name of the city
    """
    city_dict = get_city_data_API(city_name)  # creating dict to update cities table
    update_cities_table(city_dict)  # updating cities table

    api_rest_dict = {}  # TODO: from where??
    rest = RestaurantFromAPI(api_rest_dict, city_dict['location_id'])  # creating RestaurantFromAPI object

    rest_dict = rest.get_rest_for_db()
    res_id = update_restaurants_table(rest_dict)  # updating cities table + return res_id

    cuisines = rest.get_cuisines()  # getting cuisines list
    update_cuisines_table(cuisines, res_id)  # updating cuisines table

    reviews = rest.get_reviews()  # getting reviews list (list of dicts)
    update_reviews_table(reviews, res_id)  # updating reviews table

    awards = rest.get_awards()  # getting awards list
    update_awards_table(awards, res_id)  # updating awards table
