"""

Shared Mongo Connection

"""


from pymongo import MongoClient
import os


#try to fetch the below from property file

#placeholder mongo connection string
CONNSTR = 'mongodb://mongo-db:27017/'
#fetch from env varianle
USERNAME = os.getenv('MONGO_USER')
PASSWORD = os.getenv('MONGO_PASSWD')
AUTH_DB = 'admin'

CLIENT = MongoClient(CONNSTR, username=USERNAME, password=PASSWORD, authSource=AUTH_DB, maxPoolSize=10)
