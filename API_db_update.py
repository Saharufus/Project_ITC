from detailed_page_mining import update_cities_table, update_restaurants_table, \
    update_cuisines_table, update_reviews_table, update_awards_table

#TODO: insert to main with api mining, with "scrape_city_API"
#TODO: loop on cities list?? maybe add to scrape_cities_API(list_of_cities, num_rests) in API_SCRAPER

def api_update_cities_db(city): # accept city dict
    """
    Gets city details as dictionary and updates cities table in database
    @param city: city details as dictionary
    """
    update_cities_table(city)

def api_update_restaurant_db(rest_obj): # accept city dict
    """
    Gets a RestaurantFromAPI object of a single restaurant webpage from Tripadvisor and feed the db with mined data
    @param: rest_obj: RestaurantFromAPI object of a single restaurant
    """
    # city_dict = get_city_data_API(city_name)  # creating dict to update cities table
    # update_cities_table(city_dict)  # updating cities table

    # api_rest_dict = {}
    rest = rest_obj

    rest_dict = rest.get_rest_for_db()
    res_id = update_restaurants_table(rest_dict)  # updating cities table + return res_id

    cuisines = rest.get_cuisines()  # getting cuisines list
    update_cuisines_table(cuisines, res_id)  # updating cuisines table

    reviews = rest.get_reviews()  # getting reviews list (list of dicts)
    update_reviews_table(reviews, res_id)  # updating reviews table

    awards = rest.get_awards()  # getting awards list
    update_awards_table(awards, res_id)  # updating awards table
