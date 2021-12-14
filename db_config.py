# define username and password based on local mysql configuration
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'baris'
HOST = 'localhost'

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

# creating data base MySQL queries:
CREATE_DB = """CREATE DATABASE IF NOT EXISTS restaurants;"""

USE_DB = """USE restaurants;"""

CREATE_CITIES = """CREATE TABLE IF NOT EXISTS cities (
location_id int primary key unique, 
city_name varchar(255),
num_restaurants int,
timezone varchar(255),
num_reviews int,
latitude float,
longitude float
);
"""

CREATE_RES = """CREATE TABLE IF NOT EXISTS restaurants (
    res_id int auto_increment primary key,
    res_name varchar(255),
    location_id int,
    rating float,
    reviews_num int,
    price_rate varchar(50),
    city_rate int,
    address varchar(255),
    website varchar(255),
    phone varchar(255),
    latitude float,
	longitude float,
    UNIQUE (location_id, res_name, address),
    FOREIGN KEY (location_id) REFERENCES cities(location_id)
);"""

CREATE_CUIS = """CREATE TABLE IF NOT EXISTS cuisines (
    res_id int,
    cuisine varchar(255),
	FOREIGN KEY (res_id) REFERENCES restaurants(res_id)
);"""

CREATE_REV = """CREATE TABLE IF NOT EXISTS reviews (
    rev_id int primary key,
    user_name varchar(255),
    review_title varchar(255),
    res_id int,
    rate float,
    date varchar(255),
    review_text varchar(255),
	FOREIGN KEY (res_id) REFERENCES restaurants(res_id)
);"""

CREATE_AWARDS="""CREATE TABLE IF NOT EXISTS awards (
    res_id int,
    award_type varchar(255),
    year int,
	FOREIGN KEY (res_id) REFERENCES restaurants(res_id)
);"""

CREATE_DB_QUERIES_INIT = [CREATE_DB, USE_DB, CREATE_CITIES, CREATE_RES, CREATE_CUIS, CREATE_REV, CREATE_AWARDS]
