import pymysql

MAIN_PAGE = 'https://www.tripadvisor.com/'
WEBSITE_REST_URL = "https://www.tripadvisor.com/Restaurants"
RES_COLUMNS = ["Name",
               "City",
               "Rating",
               "Reviews_num",
               "Price_rate",
               "City_rate",
               "Address",
               "Website",
               "Phone"]
CUIS_COLUMNS = ['res_id', 'cuisine']
CONNECTION = pymysql.connect(host='localhost',
                             user='tripadvisorscrapper',
                             password='tradscITC2021',
                             database='restaurants',
                             cursorclass=pymysql.cursors.DictCursor)


