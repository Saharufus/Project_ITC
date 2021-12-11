from db_config import *
import pymysql


def create_db(queries=CREATE_DB_QUERIES_INIT):
    connection = pymysql.connect(host=HOST,
                                 user=MYSQL_USERNAME,
                                 password=MYSQL_PASSWORD,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    for query in queries:
        cursor.execute(query)
        connection.commit()
    print('database created successfully')
