import pymongo
from config.connection_string import connection_string

mongodb_client = pymongo.MongoClient(connection_string)
