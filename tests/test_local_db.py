import pytest
import pandas as pd
import glob

from vlcars.local_db import (create_connection,
                             create_table,
                             insert_in_database,
                             sqldb_to_dataframe)


def test_db_creation_insertion():

    # -----------------
    # init SQL database
    db_file = "tests/files/cars.db"
    conn = create_connection(db_file)
    create_table(conn)



    # --------------------------------------------------------
    # read _parsed.txt files with the mock files for each site
    mock_files = glob.glob("tests/files/*_parsed.txt")
    parsed_entries = list() # contains all the lines in *_parsed.txt files
    for file in mock_files:
        lines = [line.strip().split("\t") for line in open(file, "r").readlines()]
        # replace by int type when necessary. From [3] to [6] are all numeric values: age, km, price, power
        for line in lines:
            for i in range(3, 7):
                if line[i] != "":
                    line[i] = int(line[i])

        parsed_entries += lines

    # insert lines in SQL database
    insert_in_database(parsed_entries, conn)

    # create a DataFrame with all the lines.
    colnames = ["id", "brand", "model", "age", "km", "price", "power", "province", "fuel", "gear", "description",
                "site_url", "query_time", "site"]
    sql_query = pd.read_sql_query('''SELECT * FROM cars''', conn)
    expected_df = pd.DataFrame(sql_query, columns=colnames)
    expected_df.sort_values("id", inplace=True)



    # -----------------------------
    # Compare inserted and expected
    # get the info in the SQL database in DataFrame format, and compare it to the expected_df
    inserted_df = sqldb_to_dataframe(conn)
    inserted_df.sort_values("id", inplace=True)

    assert inserted_df.equals(expected_df)






