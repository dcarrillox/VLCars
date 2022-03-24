import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn):
    sql_create_cars_table = """ CREATE TABLE IF NOT EXISTS cars (
                                        id TEXT PRIMARY KEY,
                                        brand TEXT,
                                        model TEXT,
                                        age INTEGER,
                                        km INTEGER,
                                        price INTEGER,
                                        power INTEGER,
                                        province TEXT, 
                                        fuel TEXT,
                                        gear TEXT,
                                        description TEXT,
                                        site_url TEXT,
                                        query_time DATE,
                                        site TEXT
                                    ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_cars_table)
        c.execute(sql_create_cars_table)
    except Error as e:
        print(e)


def insert_in_database(parsed_entries, conn):

    sql_insert_car = ''' INSERT INTO cars(id,brand,model,age,km,price,power,province,fuel,gear,description,site_url,query_time,site)
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET query_time = query_time '''

    with conn:
        cur = conn.cursor()
        for car_entry in parsed_entries:
            cur.execute(sql_insert_car, car_entry)


def sqldb_to_dataframe(conn):
    sql_query = pd.read_sql_query('''SELECT * FROM cars''', conn)

    # create the dataframe
    colnames = ["id", "brand", "model", "age", "km", "price", "power", "province", "fuel", "gear", "description",
                "site_url", "query_time", "site"]
    df = pd.DataFrame(sql_query, columns=colnames)

    return df
