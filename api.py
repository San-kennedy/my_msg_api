"""
Main module to launch APIs
"""

import sys
import logging
from datetime import datetime
import falcon
from msgapi.msgapp import Message
from msgapi.specific_msg import SpecificMsg
from msgapi.mongo_db_conf import CLIENT

try:
    #Setting logging to debug
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger('myapi')
    #check if application database exists
    #if not create it before starting up
    #database name msgstore
    if ('msgstore' not in CLIENT.list_database_names()):
        dbs = CLIENT['msgstore']
        coll = dbs["defaultthroughapi"]
        coll.insert_one({'db': 'msg', "creationTimeUTC": datetime.utcnow()})
        logger.info('Created App DB')
        #naming collection as messages
        dbs.create_collection('messages')
        logger.info('Created app collection')

    logger.info("App database exists, Startin APP...")

    MSGAPI = falcon.API()

    MSG = Message()
    SPECIFICMSG = SpecificMsg()

    MSGAPI.add_route('/message', MSG)
    MSGAPI.add_route('/message/{msgId}', SPECIFICMSG)

except Exception as exp:
    logger.error("Oops we have an error " +str(exp))
    sys.exit(1)
