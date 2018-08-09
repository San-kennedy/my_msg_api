"""
Implement API for specific message request
"""

import json
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

    def on_get(self, req, res, msgId):
        """ Implement get logic"""
        try:
            obj_str = msgId
            # converting string to ObjectId typr
            oid = ObjectId(obj_str)
            #query to find the message
            result = self.messages.find_one({"_id":oid})
            if not result:
                res.body = json.dumps({"Info":"Message not found"}, ensure_ascii = False)
                res.status = falcon.HTTP_200
            else:
                #palindrome check
                if result['msg'] == result['msg'][::-1]:
                    result['palindrome'] = True
                else:
                    result['palindrome'] = False
                res.body = json.dumps(str(result), ensure_ascii = False)
                res.status = falcon.HTTP_200

        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body,ensure_ascii=False)
            res.status = falcon.HTTP_400

    def on_delete(self, req, res, msgId):
        """
            Implementing Delete logic
        """

        try:
            obj_str = msgId
            oid = ObjectId(obj_str)
            del_op = self.messages.delete_one({"_id":oid})
            if del_op.deleted_count:
                res.body = json.dumps({"deleted_msgId":msgId}, ensure_ascii=False)
                res.status = falcon.HTTP_200
            else:
                res.body = json.dumps({"info": "Message not found"}, ensure_ascii=False)
                res.status = falcon.HTTP_200
        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400