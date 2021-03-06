import pymysql
import config
from db_config import MYSQL_PASSWORD, HOST, MYSQL_USERNAME


class TableUpdate:
    def __init__(self, name, data):
        """
        @param name: table name (as the name in MySQL DB)
        @param data: data dictionary of restaurant details
        """
        self.name = name
        self.columns = data.keys()
        self._data = data
        self._connection = pymysql.connect(host=HOST,
                                           user=MYSQL_USERNAME,
                                           password=MYSQL_PASSWORD,
                                           database=config.DB,
                                           cursorclass=pymysql.cursors.DictCursor)
        self._cursor = self._connection.cursor()

    def insert_table(self):
        """
        Inserts records of data to MySQL DB
        """
        columns_sql = ','.join(self.columns)
        values = [self._data.get(col) for col in self.columns]
        values_place = (','.join(["%s" for i in range(len(self.columns))]))

        sql = f"""INSERT IGNORE INTO {self.name}({columns_sql})  
        VALUES({values_place})"""
        self._cursor.execute(sql, values)
        self._connection.commit()

    def get_last_res_id(self):
        """
        Returns last restaurant ID from MySQL DB
        """
        return self._cursor.lastrowid
