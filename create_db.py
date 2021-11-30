from db_config import *

def create_db(connection=INIT_CONNECTION, queries=CREATE_DB_QUERIES_INIT):
    cursor = connection.cursor()

    for query in queries:
        cursor.execute(query)
        connection.commit()


if __name__ == '__main__':
    create_db()
    print('database created successfully')
