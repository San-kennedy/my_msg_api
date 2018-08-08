"""
Main module to launch APIs
"""

import sys
import falcon
from msgapi.msgapp import Message
from msgapi.mongo_db_conf import CLIENT
from datetime import datetime

try:
    if ('msg' not in CLIENT.list_database_names()):
        dbs = CLIENT['msg']
        coll = dbs["defaultthroughapi"]
        coll.insert_one({'db': database, "creationTimeUTC": datetime.utcnow()})
        print('Created App DB \n')
        dbs.create_collection('messages')
        print('Created app collection \n')
    else:
        print("App database exists, Startin APP...")

    MSGAPI = falcon.API()

    MSG = Message()

    API.add_route('/message', MSG)

except Exception as exp:
    print(str(exp))
    sys.exit(1)
