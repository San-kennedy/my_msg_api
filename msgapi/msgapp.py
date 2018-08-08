"""
Implement API for general message request
"""

import json
import falcon
from msgapi.mongo_db_conf import CLIENT
import msgapi.exceptions as custexp

class Message(object):
    """
        Class to implement get,post and delete

     """

    def on_get(self, req, res):
        """ Implement get logic"""
        dbs = CLIENT['msg']
        messages = dbs['messages']
        result = ""
        for msg in messages.find().limit(15):
            #"Build resp"


