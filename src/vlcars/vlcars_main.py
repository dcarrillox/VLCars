import logging
import sys, os
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
    requiredArgs = parser.add_argument_group("Required Arguments")
    requiredArgs.add_argument('-s', '--site',
                              default=sites[0],
                              const=sites[0],
                              choices=sites,
                              nargs='?',
                              dest='site',
                              help=''
                              )

    requiredArgs.add_argument('-p', '--province',
                              default='valencia',
                              const='valencia',
                              nargs='?',
                              dest='province',
                              help=''
                              )

    args = parser.parse_args()
    return args


def main():

    SITES = sorted(
                    ["autocasion",
                     ]
    )
    args = parse_args(SITES)

    # init local_db
    #os.rmdir("/home/dani/.local/share/vlcars")
    appname = "vlcars"
    appauthor = "dcarrillox"
    db_path = user_data_dir(appname, appauthor)
    os.makedirs(db_path, exist_ok=True)
    db_file = db_path + "/cars.db"

    conn = create_connection(db_file)
    create_table(conn)


    # ------------------
    # query sites online
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



    # ----------------------------------
    # create Dash app and render results
    # print("\nRendering results.....")
    # df = sqldb_to_dataframe(conn)
    # run_server(df)





if __name__ == "__main__":
    main()