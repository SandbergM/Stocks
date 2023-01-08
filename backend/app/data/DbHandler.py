import sqlite3

___STOCKS_DB_PATH = "./app/data/stocks.db"

def multiple_insert( insert_query, data ):

    try:
        with sqlite3.connect( ___STOCKS_DB_PATH ) as connection:
            cursor = connection.cursor()
            cursor.executemany(insert_query, data)
            
    except Exception as e:
        print(e)
        return False
    
    return True

def select_query( sql_query, params = None ):

    if params is None:
        params = ()

    res = []

    with sqlite3.connect( ___STOCKS_DB_PATH ) as connection:
        conn = connection.cursor()
        output_obj = conn.execute( sql_query, params )
        results = output_obj.fetchall()
        
        for row in results:
            col_names = [tup[0] for tup in output_obj.description]
            row_values = [i for i in row]
            row_as_dict = dict(zip(col_names,row_values))
            res.append(row_as_dict)
        
    return res

def update_query( sql_update_query, data ):

    try:
        with sqlite3.connect( ___STOCKS_DB_PATH ) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_update_query, data)
            connection.commit()
    except:
        return False

    return True

def delete_query( sql_delete_query, params ):

    try:
        with sqlite3.connect( ___STOCKS_DB_PATH ) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_delete_query, params)
            connection.commit()
    except:
        return False

    return True