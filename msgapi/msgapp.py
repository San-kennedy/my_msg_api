"""
Implement API for general message request
"""

import json
import logging
import falcon
from msgapi.mongo_db_conf import CLIENT
import msgapi.exceptions as custexp

class Message(object):
    """
        Class to implement get,post and delete

     """

    dbs = CLIENT['msgstore']
    messages = dbs['messages']
    msgapp_logger = logging.getLogger('myapi.msgapp')

    def on_get(self, req, res):
        """ Implement get logic"""
        try:
            result = []
            for msg in self.messages.find().limit(15):
                result.append(msg)

            res.body = json.dumps(str(result), ensure_ascii = False)
            res.status = falcon.HTTP_200
            self.msgapp_logger.info("sending response to get on generic message")

        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_500
            self.msgapp_logger.error("Exception %s", str(body))

    def on_post(self, req, res):
        """Implement post logic"""
        try:
            #check for content type of palyload. accept only application/json
            if req.content_type != "application/json":
                raise custexp.ContentTypeUnsupported()
            request = json.load(req.stream)
            self.msgapp_logger.debug("Post received payload %s", str(request))
            #check if the content is a list of messages
            if not isinstance(request, list):
                raise custexp.IllegalArgumentException
            #check if each messages in list have a key 'msg'
            for entry in request:
                if 'msg' not in entry:
                    raise  custexp.IllegalArgumentException
            ids = self.messages.insert(request)
            res.body = json.dumps(str(ids), ensure_ascii=False)
            res.status = falcon.HTTP_200
            self.msgapp_logger.info("Post success")
            self.msgapp_logger.debug("Obj ID/s %s", str(ids))

        except Exception as exp:
            body = {"Error":str(exp)}
            res.body = json.dumps(body, ensure_ascii=False)
            res.status = falcon.HTTP_400
            self.msgapp_logger.error("Exception %s", str(body))
