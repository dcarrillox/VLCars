import logging
import sys, os, glob
import argparse
from platformdirs import *
import pandas as pd




#from vlcars import __version__

from vlcars.local_db import *
from vlcars.query_online import *
from vlcars.app import *



__author__ = "dcarrillox"
__copyright__ = "dcarrillox"
__license__ = "MIT"

_logger = logging.getLogger(__name__)




def parse_args(sites):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', '--site',
                              default=sites[0],
                              const=sites[0],
                              choices=sites,
                              nargs='?',
                              dest='site',
                              help=''
                              )

    parser.add_argument('-p', '--province',
                              default='valencia',
                              const='valencia',
                              nargs='?',
                              dest='province',
                              help=''
                              )
    parser.add_argument('-l',
                        '--local_server',
                        dest="server",
                        nargs="?",
                        default=False,
                        const=True,
                        help="read info from tabular file under 'data/' and run the app")


    parser.add_argument('--heroku',
                        nargs="?",
                        default=False,
                        const=True,
                        help="read info from tabular file under 'data/' and run the app")

    parser.add_argument("--sql_to_tsv",
                        nargs="?",
                        default=False,
                        const=True,
                        help="parse SQL database and write to tabular file in 'data/yy-mm-dd.txt'")

    args = parser.parse_args()
    return args


def main():

    SITES = sorted(
                    ["autocasion",
                     ]
    )
    args = parse_args(SITES)
    print(args)

    # init local_db
    appname = "vlcars"
    appauthor = "dcarrillox"
    db_path = user_data_dir(appname, appauthor)
    os.makedirs(db_path, exist_ok=True)
    db_file = db_path + "/cars.db"

    conn = create_connection(db_file)
    create_table(conn)



    # -----------------------------------
    # Check arguments and run accordingly

    # --heroku
    # parse tabular database to DataFrame and run app. Used by branch "heroku" to run app on Heroku.
    #args.heroku = True
    if args.heroku:
        tab_database_file = glob.glob("src/vlcars/data/*.tsv")[0]
        tab_database_df = pd.read_csv(tsv_file, sep="\t", header=0)
        run_server_heroku(tab_database_df)


    # --sql_to_tab
    # parses current SQL database to tsv in "data/yy-mm-dd.tsv"
    elif args.sql_to_tsv:
        sql_database_df = sqldb_to_dataframe(conn)
        # write to file
        tsv_out = f"src/vlcars/data/{time.strftime('%Y-%m-%d')}.tsv"
        sql_database_df.to_csv(tsv_out, header=True, index=False, sep="\t")

    # create Dash app and render results locally
    elif args.server:
        df = sqldb_to_dataframe(conn)
        run_server(df)



    # query sites online
    else:

        parsed_pages = list()


        if args.site == "autocasion":
            parsed_pages += query_online_autocasion(args.province)

            # # create the mock file for testing
            # parsed_pages = sorted(parsed_pages)
            # for page in parsed_pages:
            #     print(page)
            #
            # with open("/home/dani/effidotpy/github/VLCars/tests/files/autocasion_parsed.txt", "w") as fout:
            #     for line in parsed_pages:
            #         line[3], line[4], line[5], line[6] = str(line[3]), str(line[4]), str(line[5]), str(line[6])
            #         fout.write("\t".join(line) + "\n")


        #-----------------------------
        # insert in local SQL database
        insert_in_database(parsed_pages, conn)









if __name__ == "__main__":
    main()