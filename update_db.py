import pymysql

CONNECTION = {'HOST': 'localhost',
              'USER': 'tripadvisorscrapper',
              'PASSWORD': 'tradscITC2021',
              'DATABASE': 'restaurants',
              }

RESTAURANTS_COLS = ['res_name', 'city_name', 'rating', 'reviews_num', 'price_rate', 'city_rate', 'address', 'website', 'phone']
CUISINES_COLS = ['res_id', 'cuisine']
REVIEWS_COLS = ['rev_id', 'user_name', 'review_title', 'res_id', 'rate', 'date', 'review_text']

class TableUpdate:
    def __init__(self, name, columns, data):
        """
        name: table name (as the name in MySQL DB)
        columns: list of columns name (equals in DB and the keys of the data dict)
        data: data dictionary of restaurant details
        """
        self.name = name
        self.columns = columns
        self._data = data
        self._connection = self._sql_connection()
        self._cursor = self._connection.cursor()

        self._insert_table()


    def _sql_connection(self):
        connection = pymysql.connect(host=CONNECTION['HOST'],
                                     user=CONNECTION['USER'],
                                     password=CONNECTION['PASSWORD'],
                                     database=CONNECTION['DATABASE'],
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def _insert_table(self):
        # table = 'restaurants'
        # columns = ['res_name', 'city_name', 'rating', 'reviews_num', 'price_rate', 'city_rate', 'address', 'website', 'phone']
        columns_sql = ','.join(self.columns)
        values = [self._data.get(col) for col in self.columns]
        values_place = (','.join(["%s" for i in range(len(self.columns))]))

        sql = f"""REPLACE INTO {self.name}({columns_sql})  
        VALUES({values_place})"""
        self._cursor.execute(sql, values)

        self._connection.commit()

    def get_last_res_id(self):
        return self._cursor.lastrowid


#todo: ADD TO SCRAPE!!!!
##################################################################################################

# updating restaurants table
restaurants = TableUpdate(name='restaurants', columns=RESTAURANTS_COLS, data=data)

# getting res_id (of MySQL database)
res_id = restaurants.get_last_res_id()

# updating reviews table
for review in data.get('reviews'):
    review.update({'res_id': res_id})
    rev_update = TableUpdate(name='reviews', columns=REVIEWS_COLS, data=review)

# updating cuisines table
for cuisine in data.get('cuisines'):
    cuisines = TableUpdate(name='cuisines', columns=CUISINES_COLS, data={'res_id': res_id, 'cuisine': cuisine})

##################################################################################################




