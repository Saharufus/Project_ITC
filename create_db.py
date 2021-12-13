from db_config import *
import pymysql
import logging

logging.basicConfig(filename='Tripadvisor scraper log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', filemode='w')


def create_db(queries=CREATE_DB_QUERIES_INIT):
    connection = pymysql.connect(host=HOST,
                                 user=MYSQL_USERNAME,
                                 password=MYSQL_PASSWORD,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    for query in queries:
        cursor.execute(query)
        connection.commit()
    logging.info('database created successfully')
