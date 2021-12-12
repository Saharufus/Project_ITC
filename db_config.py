# define username and password based on local mysql configuration
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'
HOST = 'localhost'

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

# creating data base MySQL queries:
CREATE_DB = """CREATE DATABASE IF NOT EXISTS restaurants;"""

USE_DB = """USE restaurants;"""

CREATE_RES = """CREATE TABLE IF NOT EXISTS restaurants (
                res_id int auto_increment primary key,
                city_name varchar(255),
                res_name varchar(255),
                rating float,
                reviews_num int,
                price_rate varchar(50),
                city_rate int,
                address varchar(255),
                website varchar(255),
                phone varchar(255),
                UNIQUE (city_name,res_name, address)
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

CREATE_DB_QUERIES_INIT = [CREATE_DB, USE_DB, CREATE_RES, CREATE_CUIS, CREATE_REV]
