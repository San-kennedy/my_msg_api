"""
Main module to launch APIs
"""

import sys
import falcon
from msgapi.msgapp import Message
from msgapi.specific_msg import SpecificMsg
from msgapi.mongo_db_conf import CLIENT
from datetime import datetime

try:
    #check if application database exists
    #if not create it before starting up
    #database name msgstore
    if ('msgstore' not in CLIENT.list_database_names()):
        dbs = CLIENT['msgstore']
        coll = dbs["defaultthroughapi"]
        coll.insert_one({'db': 'msg', "creationTimeUTC": datetime.utcnow()})
        print('Created App DB \n')
        #naming collection as messages
        dbs.create_collection('messages')
        print('Created app collection \n')

    print("App database exists, Startin APP...")

    MSGAPI = falcon.API()

    MSG = Message()
    SPECIFICMSG = SpecificMsg()

    MSGAPI.add_route('/message', MSG)
    MSGAPI.add_route('/message/{msgId}', SPECIFICMSG)

except Exception as exp:
    print(str(exp))
    sys.exit(1)
