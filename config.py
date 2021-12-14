THREADS = 5
NEW_TAB = 1
MAIN_TAB = 0

PRICING_RATE = 0
CUISINE = 1
CITY_RATE = 0
REMOVE_HASH = 1
NUM_TO_DIVIDE_RATING = 10
DIGIT = 0
SEARCH_BOX = 1

# define username and password based on local mysql configuration
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'baris'
DB = 'restaurants'
HOST = 'localhost'

MAIN_PAGE = 'https://www.tripadvisor.com/'
WEBSITE_REST_URL = "https://www.tripadvisor.com/Restaurants"

CITIES_TAB = 'cities'
RES_TAB = 'restaurants'
CUIS_TAB = 'cuisines'
REV_TAB = 'reviews'
AWARDS_TAB = 'awards'

CITIES_COLS = ['location_id',
               'city_name',
               'num_restaurants',
               'timezone varchar',
               'num_reviews',
               'latitude',
               'longitude']

RESTAURANTS_COLS = ['res_name',
                    'location_id',
                    'rating',
                    'reviews_num',
                    'price_rate',
                    'city_rate',
                    'address',
                    'website',
                    'phone',
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

CUIS_FROM_TUPLE = 0
CITIES_FOR_SCRAPER = 2
MAX_CHARS = 255