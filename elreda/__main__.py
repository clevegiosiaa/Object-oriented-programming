from kink import di

from elreda.uis import GUI_V1
from elreda.services import OrderService
from mock_db import MockDB
from elreda.uis_v2 import GUI_V2

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dbinit")
    parser.add_argument("-dburl")
    args = parser.parse_args()
    dbinit = args.dbinit
    dburl = args.dburl
    if dburl is not None:
        dburl = dburl.lower()

    if dbinit is not None:
        dbinit = dbinit.lower()
        if dbinit == 'true':
            di['_db_setting'] = dburl
            order_service = OrderService()
            order_service.initialise_new_database()

        elif dbinit == "false":
            di["_order_db"] = MockDB()
    else:
        di['_db_setting'] = dburl

    ui = GUI_V2()
    ui.start()
