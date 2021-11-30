import pymysql

MAIN_PAGE = 'https://www.tripadvisor.com/'
WEBSITE_REST_URL = "https://www.tripadvisor.com/Restaurants"

DB = 'restaurants'
RES_TAB = 'restaurants'
CUIS_TAB = 'cuisines'
REV_TAB = 'reviews'


RESTAURANTS_COLS = ['res_name',
                    'city_name',
                    'rating',
                    'reviews_num',
                    'price_rate',
                    'city_rate',
                    'address',
                    'website',
                    'phone']

CUISINES_COLS = ['res_id',
                 'cuisine']

REVIEWS_COLS = ['rev_id',
                'user_name',
                'review_title',
                'res_id',
                'rate',
                'date',
                'review_text']

CONNECTION = pymysql.connect(host='localhost',
                             user='tripadvisorscrapper',
                             password='tradscITC2021',
                             database='restaurants',
                             cursorclass=pymysql.cursors.DictCursor)

# creating data base MySQL queries:
CREATE_DB = """CREATE DATABASE restaurants;"""

USE_DB = """USE restaurants;"""

CREATE_RES = """CREATE TABLE restaurants (
                tab_col[0] int auto_increment primary key,
                city_name varchar(255),
                res_name varchar(255),
                rating float,
                reviews_num int,
                price_rate varchar(50),
                city_rate int,
                address varchar(255),
                website varchar(255),
                phone varchar(255)
            );"""

CREATE_CUIS = """CREATE TABLE cuisines (
                        res_id int,
                        cuisine varchar(255),
                    	FOREIGN KEY (res_id) REFERENCES restaurants(res_id)
                    );"""

CREATE_REV = """CREATE TABLE reviews (
                        rev_id int primary key,
                        user_name varchar(255),
                        review_title varchar(255),
                        res_id int,
                        rate float,
                        date varchar(255),
                        review_text varchar(255),
                        FOREIGN KEY (res_id) REFERENCES restaurants(res_id)
                    );"""

CREATE_DB_QUERIES = [CREATE_DB, USE_DB, CREATE_RES, CREATE_CUIS, CREATE_REV]


