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

    dbs = CLIENT['msgstore']
    messages = dbs['messages']

    def on_get(self, req, res):
        """ Implement get logic"""
        try:
            result = []
            for msg in self.messages.find().limit(15):
                result.append(msg)

            res.body = json.dumps(str(result), ensure_ascii = False)
            res.status = falcon.HTTP_200

        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body,ensure_ascii=False)
            res.status = falcon.HTTP_500

    def on_post(self,req,res):

        try:
            if req.content_type != "application/json":
                raise custexp.ContentTypeUnsupported()
            request = json.load(req.stream)
            ids = self.messages.insert(request)
            res.body = json.dumps(str(ids),ensure_ascii=False)
            res.status = falcon.HTTP_200

        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body,ensure_ascii=False)
            res.status = falcon.HTTP_400







