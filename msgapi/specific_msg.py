"""
Implement API for specific message request
"""

import json
import string
import logging
import falcon
from bson import ObjectId
from msgapi.mongo_db_conf import CLIENT

class SpecificMsg(object):
    """
        Class to implement get and delete
        for specific message referred by ObjID
    """

    dbs = CLIENT['msgstore']
    messages = dbs['messages']
    specificmsgapp_logger = logging.getLogger('myapi.msgapp.specific_msg')

    @classmethod
    def palindrome_test(cls, msg_str):
        letters = set(string.ascii_lowercase)
        msg_str_lower = msg_str.lower()
        processed_str = ""
        for char in msg_str_lower:
            if char in letters:
                processed_str+=char
        return processed_str == processed_str[::-1]

    def on_get(self, req, res, msgId):
        """ Implement get logic"""
        try:
            obj_str = msgId
            # converting string to ObjectId typr
            oid = ObjectId(obj_str)
            self.specificmsgapp_logger.debug("Received msgID %s", obj_str)
            #query to find the message
            result = self.messages.find_one({"_id":oid})
            if not result:
                res.body = json.dumps({"Info":"Message not found"}, ensure_ascii = False)
                res.status = falcon.HTTP_404
                self.specificmsgapp_logger.warning("Message with ID %s not found", obj_str)
            else:
                #palindrome check
                if self.palindrome_test(result['msg']):
                    result['palindrome'] = True
                else:
                    result['palindrome'] = False
                res.body = json.dumps(str(result), ensure_ascii = False)
                res.status = falcon.HTTP_200
                self.specificmsgapp_logger.info("Message returned")
                self.specificmsgapp_logger.debug("Message with ID %s returned", obj_str)

        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400
            self.specificmsgapp_logger.error("Exception %s", str(body))

    def on_delete(self, req, res, msgId):
        """
            Implementing Delete logic
        """

        try:
            obj_str = msgId
            oid = ObjectId(obj_str)
            self.specificmsgapp_logger.debug("Received msgID %s", obj_str)
            del_op = self.messages.delete_one({"_id":oid})
            if del_op.deleted_count:
                res.body = json.dumps({"deleted_msgId":msgId}, ensure_ascii=False)
                res.status = falcon.HTTP_200
                self.specificmsgapp_logger.info("Deleted Msg")
                self.specificmsgapp_logger.debug("Message wit ID %s deleted", obj_str)
            else:
                res.body = json.dumps({"info": "Message not found"}, ensure_ascii=False)
                res.status = falcon.HTTP_404
                self.specificmsgapp_logger.warning("Message wit ID %s not found", obj_str)
        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400
            self.specificmsgapp_logger.error("Exception %s", str(body))
