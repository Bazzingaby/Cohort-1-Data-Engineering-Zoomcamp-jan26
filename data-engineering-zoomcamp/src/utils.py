def connect_to_db(host, database, user, password):
    import psycopg2
    from psycopg2 import sql

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()

def fetch_query_results(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error fetching query results: {e}")
        return None
    finally:
        cursor.close()