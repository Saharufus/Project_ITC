def create_db(connection=CONNECTION, queries=CREATE_DB_QUERIES):
    connection.cursor()

    for query in queries:
        cursor.exequte(query)
        connection.commit()
